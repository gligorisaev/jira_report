import React, { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Upload, FileText, Activity, AlertCircle, CheckCircle, Target, Eye, Filter } from 'lucide-react';
import Papa from 'papaparse';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [activeView, setActiveView] = useState('overview');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedParent, setSelectedParent] = useState('all');

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const csvText = e.target.result;
      const parsed = Papa.parse(csvText, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        delimiter: ';'
      });

      const processedData = parsed.data.map((row, index) => ({
        id: index,
        parentKey: row['Parent Requirement Key'] || null,
        parentSummary: row['Parent Requirement Summary'] || null,
        requirementKey: row['Requirement Key'],
        requirementSummary: row['Requirement Summary'],
        requirementStatus: row['Requirement Status'],
        testKey: row['Test Key'] || null,
        testSummary: row['Test Summary'] || null,
        testStatus: row['Test Status'] || null,
        defectKeys: row['Defect Keys'] || null,
        isParent: !row['Parent Requirement Key'] && row['Requirement Key'],
        hasCoverage: !!row['Test Key']
      }));

      setData(processedData);
      setFilteredData(processedData);
    };
    reader.readAsText(file);
  };

  const analytics = useMemo(() => {
    if (!filteredData.length) return null;

    const statusCounts = filteredData.reduce((acc, item) => {
      acc[item.requirementStatus] = (acc[item.requirementStatus] || 0) + 1;
      return acc;
    }, {});

    const coverageStats = {
      covered: filteredData.filter(item => item.hasCoverage).length,
      uncovered: filteredData.filter(item => !item.hasCoverage).length,
      total: filteredData.length
    };

    const parentGroups = filteredData.reduce((acc, item) => {
      const key = item.parentKey || 'Root Requirements';
      if (!acc[key]) {
        acc[key] = {
          name: item.parentSummary || 'Root Requirements',
          children: [],
          covered: 0,
          total: 0
        };
      }
      acc[key].children.push(item);
      acc[key].total += 1;
      if (item.hasCoverage) acc[key].covered += 1;
      return acc;
    }, {});

    return {
      statusCounts,
      coverageStats,
      parentGroups,
      coveragePercentage: Math.round((coverageStats.covered / coverageStats.total) * 100)
    };
  }, [filteredData]);

  const applyFilters = () => {
    let filtered = [...data];
    
    if (selectedStatus !== 'all') {
      filtered = filtered.filter(item => item.requirementStatus === selectedStatus);
    }
    
    if (selectedParent !== 'all') {
      filtered = filtered.filter(item => 
        item.parentKey === selectedParent || (!item.parentKey && selectedParent === 'root')
      );
    }
    
    setFilteredData(filtered);
  };

  React.useEffect(() => {
    applyFilters();
  }, [selectedStatus, selectedParent, data]);

  const renderOverview = () => {
    if (!analytics) return (
      <div className="p-8 text-center text-gray-500">
        <Upload className="h-16 w-16 mx-auto mb-4 text-gray-300" />
        <h3 className="text-xl font-medium mb-2">Upload a CSV file to get started</h3>
        <p>Select your Jira/Xray traceability report to visualize requirements coverage</p>
      </div>
    );

    const statusChartData = Object.entries(analytics.statusCounts).map(([status, count]) => ({
      name: status,
      value: count,
      percentage: Math.round((count / filteredData.length) * 100)
    }));

    const coverageData = [
      { name: 'Covered', value: analytics.coverageStats.covered, color: '#22c55e' },
      { name: 'Uncovered', value: analytics.coverageStats.uncovered, color: '#ef4444' }
    ];

    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-3 grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow border">
            <div className="flex items-center">
              <Target className="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <p className="text-2xl font-bold">{filteredData.length}</p>
                <p className="text-sm text-gray-600">Total Requirements</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow border">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-green-600 mr-3" />
              <div>
                <p className="text-2xl font-bold">{analytics.coverageStats.covered}</p>
                <p className="text-sm text-gray-600">Test Coverage</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow border">
            <div className="flex items-center">
              <AlertCircle className="h-8 w-8 text-orange-600 mr-3" />
              <div>
                <p className="text-2xl font-bold">{analytics.coverageStats.uncovered}</p>
                <p className="text-sm text-gray-600">Uncovered</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow border">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-purple-600 mr-3" />
              <div>
                <p className="text-2xl font-bold">{analytics.coveragePercentage}%</p>
                <p className="text-sm text-gray-600">Coverage Rate</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <h3 className="text-lg font-semibold mb-4">Requirement Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={statusChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value, name) => [`${value} (${statusChartData.find(d => d.name === name)?.percentage}%)`, 'Count']} />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <h3 className="text-lg font-semibold mb-4">Test Coverage Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={coverageData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {coverageData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <h3 className="text-lg font-semibold mb-4">Coverage by Parent Group</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {Object.entries(analytics.parentGroups).map(([key, group]) => {
              const coverage = Math.round((group.covered / group.total) * 100);
              return (
                <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <div className="flex-1">
                    <p className="font-medium text-sm truncate">{group.name}</p>
                    <p className="text-xs text-gray-600">{group.covered}/{group.total} covered</p>
                  </div>
                  <div className="ml-4">
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-green-600 h-2 rounded-full" 
                        style={{ width: `${coverage}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-center mt-1">{coverage}%</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Jira/Xray Traceability Dashboard</h1>
              <p className="mt-1 text-sm text-gray-600">Requirements coverage and test traceability analysis</p>
            </div>
            
            <div className="flex items-center space-x-4">
              <label className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer">
                <Upload className="h-5 w-5 mr-2" />
                Upload CSV
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex space-x-1 mb-6">
          {[
            { id: 'overview', label: 'Overview', icon: Activity }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveView(id)}
              className={`flex items-center px-4 py-2 rounded-lg font-medium ${
                activeView === id
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Icon className="h-5 w-5 mr-2" />
              {label}
            </button>
          ))}
        </div>

        {data.length > 0 && (
          <div className="bg-white p-4 rounded-lg shadow border mb-6">
            <div className="flex items-center space-x-4">
              <Filter className="h-5 w-5 text-gray-600" />
              
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Status</option>
                {Object.keys(analytics?.statusCounts || {}).map(status => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>

              <div className="flex-1"></div>
              
              <div className="text-sm text-gray-600">
                Showing {filteredData.length} of {data.length} requirements
              </div>
            </div>
          </div>
        )}

        <div>
          {renderOverview()}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
