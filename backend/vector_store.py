"""
Vector store module for SmartShift.
Handles ChromaDB integration for semantic worker skill matching.
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pandas as pd
from typing import List, Dict, Optional
from config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL


class WorkerVectorStore:
    """ChromaDB vector store for worker skill matching."""
    
    def __init__(self):
        """Initialize the vector store with ChromaDB client and embedding model."""
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.collection = None
    
    def initialize_collection(self):
        """Create or get ChromaDB collection."""
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(name=CHROMA_COLLECTION_NAME)
            print(f"Loaded existing collection: {CHROMA_COLLECTION_NAME}")
        except:
            # Create new collection if it doesn't exist
            self.collection = self.client.create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"description": "Warehouse worker skills and profiles"}
            )
            print(f"Created new collection: {CHROMA_COLLECTION_NAME}")
    
    def create_worker_document(self, worker: Dict) -> str:
        """
        Create searchable document from worker profile.
        
        Args:
            worker: Dictionary containing worker data
            
        Returns:
            Formatted document string for embedding
        """
        doc = f"""Worker {worker['name']}. 
        Primary skill: {worker['primary_skill']}. 
        Transferable skills: {worker['transferable_skills']}. 
        Education: {worker['education']}. 
        Physicality: {worker['physicality']}. 
        Zone: {worker['current_zone']}. 
        Function: {worker['zone_function']}.
        Shift: {worker['shift']} ({worker['shift_hours']}).
        Load: {worker['load_status']} ({worker['load_percentage']}%).
        Available: {worker['available']}."""
        return doc
    
    def index_workers(self, workers_df: pd.DataFrame):
        """
        Index all workers in ChromaDB.
        
        Args:
            workers_df: DataFrame containing worker data
        """
        if self.collection is None:
            raise ValueError("Collection not initialized. Call initialize_collection() first.")
        
        # Clear existing data
        try:
            existing_ids = self.collection.get()['ids']
            if existing_ids:
                self.collection.delete(ids=existing_ids)
                print(f"Cleared {len(existing_ids)} existing records")
        except:
            pass
        
        documents = []
        metadatas = []
        ids = []
        
        for _, worker in workers_df.iterrows():
            worker_dict = worker.to_dict()
            doc = self.create_worker_document(worker_dict)
            documents.append(doc)
            
            # Convert all metadata values to strings for ChromaDB compatibility
            metadata = {
                'worker_id': str(worker_dict['worker_id']),
                'name': str(worker_dict['name']),
                'age': str(worker_dict['age']),
                'primary_skill': str(worker_dict['primary_skill']),
                'transferable_skills': str(worker_dict['transferable_skills']),
                'education': str(worker_dict['education']),
                'physicality': str(worker_dict['physicality']),
                'current_zone': str(worker_dict['current_zone']),
                'zone_function': str(worker_dict['zone_function']),
                'shift': str(worker_dict['shift']),
                'shift_hours': str(worker_dict['shift_hours']),
                'load_status': str(worker_dict['load_status']),
                'load_percentage': str(worker_dict['load_percentage']),
                'available': str(worker_dict['available'])
            }
            metadatas.append(metadata)
            ids.append(str(worker_dict['worker_id']))
        
        # Generate embeddings
        print(f"Generating embeddings for {len(documents)} workers...")
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully indexed {len(documents)} workers in ChromaDB")
    
    def search_workers(
        self, 
        query: str, 
        exclude_zone: Optional[str] = None,
        n_results: int = 5
    ) -> List[Dict]:
        """
        Search for workers matching query.
        
        Args:
            query: Natural language description of needed skill
            exclude_zone: Zone to exclude from results (e.g., "Zone A")
            n_results: Number of results to return
            
        Returns:
            List of worker metadata dictionaries
        """
        if self.collection is None:
            raise ValueError("Collection not initialized. Call initialize_collection() first.")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Build where filter - only filter by availability
        where_filter = {"available": "Yes"}
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results * 2,  # Get more results to filter
            where=where_filter
        )
        
        # Post-process to exclude zone if specified
        filtered_results = []
        if results['metadatas'] and results['metadatas'][0]:
            for metadata in results['metadatas'][0]:
                if exclude_zone and metadata.get('current_zone') == exclude_zone:
                    continue
                filtered_results.append(metadata)
                if len(filtered_results) >= n_results:
                    break
        
        return filtered_results
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary containing collection statistics
        """
        if self.collection is None:
            return {"error": "Collection not initialized"}
        
        count = self.collection.count()
        return {
            "collection_name": CHROMA_COLLECTION_NAME,
            "total_workers": count,
            "embedding_model": EMBEDDING_MODEL
        }
    
    def reset_collection(self):
        """Delete and recreate the collection."""
        try:
            self.client.delete_collection(name=CHROMA_COLLECTION_NAME)
            print(f"Deleted collection: {CHROMA_COLLECTION_NAME}")
        except:
            pass
        self.initialize_collection()

# Made with Bob
