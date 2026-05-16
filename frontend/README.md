# SmartShift Frontend

Next.js frontend for the SmartShift AI-Powered Warehouse Workforce Rebalancing System.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Backend API running on port 8000

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment**:
   - Copy `.env.local` and update `NEXT_PUBLIC_API_URL` if needed
   - For local development: `http://localhost:8000`
   - For production: Your Render/Railway backend URL

3. **Run development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**:
   - Visit http://localhost:3000

## 📁 Project Structure

```
smartshift-frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main dashboard page
│   └── globals.css         # Global styles
├── components/
│   ├── WorkforceOverview.tsx      # Dashboard overview
│   ├── WorkerTable.tsx            # Worker data table
│   ├── OverloadForm.tsx           # Overload input form
│   └── RecommendationDisplay.tsx  # AI recommendations
├── lib/
│   └── api.ts              # API client
└── .env.local              # Environment variables
```

## 🔧 Configuration

### Environment Variables

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production deployment, update to your backend URL:
```env
NEXT_PUBLIC_API_URL=https://your-api.onrender.com
```

## 🧪 Testing

1. **Make sure backend is running**:
   ```bash
   # In backend directory
   python api.py
   ```

2. **Start frontend**:
   ```bash
   npm run dev
   ```

3. **Test features**:
   - View workforce overview
   - Filter workers
   - Submit overload request
   - View AI recommendations

## 🚀 Deployment to Vercel

### Option 1: Via Vercel Dashboard

1. Push code to GitHub
2. Go to https://vercel.com/
3. Click "Import Project"
4. Select your repository
5. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = your backend URL
6. Deploy

### Option 2: Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Add environment variable
vercel env add NEXT_PUBLIC_API_URL

# Deploy to production
vercel --prod
```

## 📦 Build for Production

```bash
npm run build
npm start
```

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Deployment**: Vercel

## 🔗 API Endpoints Used

- `GET /api/workers` - Get all workers
- `GET /api/zones/{zone}` - Get zone statistics
- `POST /api/search` - Search workers
- `POST /api/recommendations` - Get AI recommendations

## 🐛 Troubleshooting

### "Failed to load workers"
- Make sure backend is running on port 8000
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Verify CORS is enabled in backend

### "Network Error"
- Backend might not be running
- Check if backend URL is accessible
- Verify firewall/network settings

### Build Errors
- Run `npm install` to ensure all dependencies are installed
- Delete `.next` folder and rebuild
- Check Node.js version (18+ required)

## 📝 Development

### Adding New Components

1. Create component in `components/` directory
2. Import in `app/page.tsx`
3. Use TypeScript for type safety

### Modifying API Client

Edit `lib/api.ts` to add new endpoints or modify existing ones.

### Styling

- Uses Tailwind CSS utility classes
- Global styles in `app/globals.css`
- Component-specific styles inline

## 🎨 Features

- ✅ Real-time workforce overview
- ✅ Interactive worker table with filters
- ✅ Natural language overload reporting
- ✅ AI-powered recommendations
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states

## 📄 License

Part of SmartShift v2.0 project

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

---

**Built with Next.js and ❤️**
