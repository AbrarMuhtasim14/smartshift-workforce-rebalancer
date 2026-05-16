'use client';

import { useState } from 'react';
import { Worker } from '@/lib/api';
import { Download, Filter, ChevronLeft, ChevronRight } from 'lucide-react';

interface WorkerTableProps {
  workers: Worker[];
}

export default function WorkerTable({ workers }: WorkerTableProps) {
  const [zoneFilter, setZoneFilter] = useState<string[]>(['Zone A', 'Zone B', 'Zone C', 'Zone D']);
  const [loadFilter, setLoadFilter] = useState<string[]>(['Low', 'Medium', 'High']);
  const [availabilityFilter, setAvailabilityFilter] = useState<string[]>(['Yes', 'No']);
  const [currentPage, setCurrentPage] = useState(1);
  const workersPerPage = 10;

  const filteredWorkers = workers.filter(worker =>
    zoneFilter.includes(worker.current_zone) &&
    loadFilter.includes(worker.load_status) &&
    availabilityFilter.includes(worker.available)
  );

  // Pagination calculations
  const totalPages = Math.ceil(filteredWorkers.length / workersPerPage);
  const startIndex = (currentPage - 1) * workersPerPage;
  const endIndex = startIndex + workersPerPage;
  const currentWorkers = filteredWorkers.slice(startIndex, endIndex);

  // Reset to page 1 when filters change
  const handleFilterChange = (value: string, currentFilters: string[], setFilters: (filters: string[]) => void) => {
    toggleFilter(value, currentFilters, setFilters);
    setCurrentPage(1);
  };

  const handleDownload = () => {
    const csv = [
      Object.keys(filteredWorkers[0] || {}).join(','),
      ...filteredWorkers.map(worker => Object.values(worker).join(','))
    ].join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'workforce_data.csv';
    a.click();
  };

  const toggleFilter = (value: string, currentFilters: string[], setFilters: (filters: string[]) => void) => {
    if (currentFilters.includes(value)) {
      setFilters(currentFilters.filter(f => f !== value));
    } else {
      setFilters([...currentFilters, value]);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">👥 Worker Details</h2>
        <button
          onClick={handleDownload}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Download className="w-4 h-4" />
          Download CSV
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
        <div className="flex items-center gap-2 mb-3">
          <Filter className="w-5 h-5 text-gray-600" />
          <h3 className="font-semibold text-gray-900">Filters</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Zone Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Zone</label>
            <div className="flex flex-wrap gap-2">
              {['Zone A', 'Zone B', 'Zone C', 'Zone D'].map(zone => (
                <button
                  key={zone}
                  onClick={() => handleFilterChange(zone, zoneFilter, setZoneFilter)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    zoneFilter.includes(zone)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {zone}
                </button>
              ))}
            </div>
          </div>

          {/* Load Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Load Status</label>
            <div className="flex flex-wrap gap-2">
              {['Low', 'Medium', 'High'].map(load => (
                <button
                  key={load}
                  onClick={() => handleFilterChange(load, loadFilter, setLoadFilter)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    loadFilter.includes(load)
                      ? load === 'High' ? 'bg-red-600 text-white' :
                        load === 'Medium' ? 'bg-yellow-600 text-white' :
                        'bg-green-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {load}
                </button>
              ))}
            </div>
          </div>

          {/* Availability Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Availability</label>
            <div className="flex flex-wrap gap-2">
              {['Yes', 'No'].map(avail => (
                <button
                  key={avail}
                  onClick={() => handleFilterChange(avail, availabilityFilter, setAvailabilityFilter)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    availabilityFilter.includes(avail)
                      ? avail === 'Yes' ? 'bg-green-600 text-white' : 'bg-gray-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {avail}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Zone</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Primary Skill</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Shift</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Load</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Available</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {currentWorkers.map((worker) => (
                <tr key={worker.worker_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{worker.worker_id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{worker.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{worker.current_zone}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{worker.primary_skill}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{worker.shift}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      worker.load_status === 'High' ? 'bg-red-100 text-red-800' :
                      worker.load_status === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {worker.load_status} ({worker.load_percentage}%)
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      worker.available === 'Yes' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {worker.available}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {/* Pagination */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <p className="text-sm text-gray-700">
              Showing <span className="font-medium">{startIndex + 1}</span> to <span className="font-medium">{Math.min(endIndex, filteredWorkers.length)}</span> of <span className="font-medium">{filteredWorkers.length}</span> workers
            </p>
          </div>
          
          {totalPages > 1 && (
            <div className="flex items-center gap-2">
              <button
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="p-2 rounded-lg border border-gray-300 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              
              <span className="text-sm text-gray-700">
                Page <span className="font-medium">{currentPage}</span> of <span className="font-medium">{totalPages}</span>
              </span>
              
              <button
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                className="p-2 rounded-lg border border-gray-300 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Made with Bob
