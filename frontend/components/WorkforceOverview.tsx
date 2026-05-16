import { Worker } from '@/lib/api';
import { Users, UserCheck, AlertTriangle, Activity } from 'lucide-react';

interface WorkforceOverviewProps {
  workers: Worker[];
}

export default function WorkforceOverview({ workers }: WorkforceOverviewProps) {
  const totalWorkers = workers.length;
  const availableWorkers = workers.filter(w => w.available === 'Yes').length;
  const highLoadWorkers = workers.filter(w => w.load_status === 'High').length;
  const avgLoad = workers.reduce((sum, w) => sum + w.load_percentage, 0) / totalWorkers;

  const zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D'];
  const zoneStats = zones.map(zone => {
    const zoneWorkers = workers.filter(w => w.current_zone === zone);
    return {
      zone,
      total: zoneWorkers.length,
      available: zoneWorkers.filter(w => w.available === 'Yes').length,
      avgLoad: zoneWorkers.reduce((sum, w) => sum + w.load_percentage, 0) / zoneWorkers.length || 0,
    };
  });

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">📊 Workforce Overview</h2>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Workers</p>
              <p className="text-3xl font-bold text-gray-900">{totalWorkers}</p>
            </div>
            <Users className="w-12 h-12 text-blue-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Available</p>
              <p className="text-3xl font-bold text-green-600">{availableWorkers}</p>
            </div>
            <UserCheck className="w-12 h-12 text-green-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">High Load</p>
              <p className="text-3xl font-bold text-red-600">{highLoadWorkers}</p>
            </div>
            <AlertTriangle className="w-12 h-12 text-red-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Average Load</p>
              <p className="text-3xl font-bold text-gray-900">{avgLoad.toFixed(1)}%</p>
            </div>
            <Activity className="w-12 h-12 text-purple-500" />
          </div>
        </div>
      </div>

      {/* Zone Distribution */}
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Zone Distribution</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {zoneStats.map(({ zone, total, available, avgLoad }) => (
            <div key={zone} className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-2">{zone}</h4>
              <div className="space-y-1 text-sm">
                <p className="text-gray-600">Workers: <span className="font-medium text-gray-900">{total}</span></p>
                <p className="text-gray-600">Available: <span className="font-medium text-green-600">{available}</span></p>
                <p className="text-gray-600">Avg Load: <span className="font-medium text-gray-900">{avgLoad.toFixed(1)}%</span></p>
              </div>
              {/* Load bar */}
              <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${
                    avgLoad >= 70 ? 'bg-red-500' : 
                    avgLoad >= 50 ? 'bg-yellow-500' : 
                    'bg-green-500'
                  }`}
                  style={{ width: `${Math.min(avgLoad, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Made with Bob
