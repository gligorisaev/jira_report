import React, { useState, useMemo, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, TreemapChart, Treemap } from 'recharts';
import { Upload, FileText, Activity, AlertCircle, CheckCircle, Clock, Target, Eye, Filter, Download } from 'lucide-react';
import Papa from 'papaparse';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [activeView, setActiveView] = useState('overview');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedParent, setSelectedParent] = useState('all');

  // Color schemes for different statuses
  const statusColors = {
    'UNCOVERED': '#ef4444', // Red
    'NOTRUN': '#f97316',    // Orange
    'PASS': '#22c55e',      // Green
    'FAIL': '#dc2626',      // Dark Red
    'TODO': '#3b82f6',      // Blue
    'TO DO': '#3b82f6',     // Blue (alias for TODO)
    'BLOCKED': '#6b7280',   // Gray
    'RUNNING': '#eab308'    // Yellow
  };

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
        delimiter: ';' // Ensure this matches your CSV delimiter
      });

      // Process data to ensure consistent keys and add derived properties
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
        // Determine if it's a parent requirement (has a key but no parent key)
        isParent: !!row['Requirement Key'] && !row['Parent Requirement Key'],
        // Determine if it has test coverage
        hasCoverage: !!row['Test Key']
      }));

      setData(processedData);
      setFilteredData(processedData); // Initialize filtered data with all data
    };
    reader.readAsText(file);
  };

  // Analytics computations using useMemo for performance
  const analytics = useMemo(() => {
    if (!filteredData.length) return null;

    // Count occurrences of each requirement status
    const statusCounts = filteredData.reduce((acc, item) => {
      acc[item.requirementStatus] = (acc[item.requirementStatus] || 0) + 1;
      return acc;
    }, {});

    // Count occurrences of each test status (only for items with a test status)
    const testStatusCounts = filteredData
      .filter(item => item.testStatus)
      .reduce((acc, item) => {
        acc[item.testStatus] = (acc[item.testStatus] || 0) + 1;
        return acc;
      }, {});

    // Calculate overall test coverage statistics
    const coverageStats = {
      covered: filteredData.filter(item => item.hasCoverage).length,
      uncovered: filteredData.filter(item => !item.hasCoverage).length,
      total: filteredData.length
    };

    // Group requirements by their parent, creating a hierarchical view
    const parentGroups = filteredData.reduce((acc, item) => {
      const key = item.parentKey || 'Root Requirements'; // Use 'Root Requirements' for top-level items
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
      testStatusCounts,
      coverageStats,
      parentGroups,
      coveragePercentage: Math.round((coverageStats.covered / coverageStats.total) * 100) || 0
    };
  }, [filteredData]); // Recalculate only when filteredData changes

  // Filter handlers
  const applyFilters = () => {
    let filtered = [...data]; // Start with the original data

    // Apply status filter
    if (selectedStatus !== 'all') {
      filtered = filtered.filter(item => item.requirementStatus === selectedStatus);
    }

    // Apply parent filter
    if (selectedParent !== 'all') {
      filtered = filtered.filter(item =>
        item.parentKey === selectedParent || (!item.parentKey && selectedParent === 'root')
      );
    }

    setFilteredData(filtered);
  };

  // Apply filters whenever selectedStatus, selectedParent, or the raw data changes
  useEffect(() => {
    applyFilters();
  }, [selectedStatus, selectedParent, data]); // eslint-disable-line react-hooks/exhaustive-deps

  // Helper function to render the Overview tab content
  const renderOverview = () => {
    if (!analytics) return <div className="p-8 text-center text-gray-500">Upload a CSV file to get started</div>;

    // Prepare data for status distribution chart
    const statusChartData = Object.entries(analytics.statusCounts).map(([status, count]) => ({
      name: status,
      value: count,
      percentage: Math.round((count / filteredData.length) * 100)
    }));

    // Prepare data for coverage pie chart
    const coverageData = [
      { name: 'Covered', value: analytics.coverageStats.covered, color: '#22c55e' }, // Green
      { name: 'Uncovered', value: analytics.coverageStats.uncovered, color: '#ef4444' } // Red
    ];

    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {/* Key Metrics Section */}
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

        {/* Status Distribution Chart */}
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

        {/* Coverage Pie Chart */}
        <div className="bg-white p-6 rounded-lg shadow border">
          <h3 className="text-lg font-semibold mb-4">Test Coverage Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={coverageData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name} ${percentage}%`}
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

        {/* Parent Groups Coverage */}
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

  // Helper function to render the Hierarchy tab content
  const renderHierarchy = () => {
    if (!analytics) return <div className="p-8 text-center text-gray-500">No data available</div>;

    return (
      <div className="bg-white rounded-lg shadow border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">Requirements Hierarchy</h3>
        </div>
        <div className="p-6">
          {Object.entries(analytics.parentGroups).map(([key, group]) => (
            <div key={key} className="mb-6">
              <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg mb-3">
                <div className="flex items-center">
                  <FileText className="h-5 w-5 text-blue-600 mr-3" />
                  <div>
                    <h4 className="font-semibold text-blue-900">{group.name}</h4>
                    <p className="text-sm text-blue-700">{group.total} requirements, {group.covered} covered</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    {Math.round((group.covered / group.total) * 100)}% covered
                  </span>
                </div>
              </div>
              
              <div className="ml-8 space-y-2">
                {group.children.map((child) => (
                  <div key={child.id} className="flex items-center justify-between p-3 border border-gray-200 rounded">
                    <div className="flex items-center flex-1">
                      <div className={`w-3 h-3 rounded-full mr-3 ${child.hasCoverage ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      <div className="flex-1">
                        <p className="font-medium text-sm">{child.requirementKey}</p>
                        <p className="text-xs text-gray-600 truncate">{child.requirementSummary}</p>
                      </div>
                    </div>
                    <div className="ml-4 flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        statusColors[child.requirementStatus] ? 
                        `bg-${statusColors[child.requirementStatus].replace('#', '')}-100 text-${statusColors[child.requirementStatus].replace('#', '')}-800` : 'bg-gray-100 text-gray-800'
                      }`}>
                        {child.requirementStatus}
                      </span>
                      {child.testKey && (
                        <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                          {child.testKey}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Helper function to render the Details Table tab content
  const renderDetailsTable = () => {
    return (
      <div className="bg-white rounded-lg shadow border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">Detailed Requirements View</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Requirement</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Summary</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Coverage</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredData.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {item.requirementKey}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                    {item.requirementSummary}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      item.requirementStatus === 'UNCOVERED' ? 'bg-red-100 text-red-800' :
                      item.requirementStatus === 'NOTRUN' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {item.requirementStatus}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.testKey || '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {item.testStatus ? (
                      <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                        {item.testStatus}
                      </span>
                    ) : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {item.hasCoverage ? (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-red-500" />
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
                {/* Hidden file input that triggers file selection */}
                <input type="file" className="hidden" accept=".csv" onChange={handleFileUpload} />
                <Upload className="h-5 w-5 mr-2" />
                Upload CSV
              </label>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        {/* Navigation Buttons */}
        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setActiveView('overview')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${activeView === 'overview' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'}`}
          >
            <Eye className="inline-block h-4 w-4 mr-2" /> Overview
          </button>
          <button
            onClick={() => setActiveView('hierarchy')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${activeView === 'hierarchy' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'}`}
          >
            <FileText className="inline-block h-4 w-4 mr-2" /> Hierarchy
          </button>
          <button
            onClick={() => setActiveView('details')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${activeView === 'details' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'}`}
          >
            <FileText className="inline-block h-4 w-4 mr-2" /> Details Table
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white p-6 rounded-lg shadow border mb-6 flex items-center space-x-4">
          <Filter className="h-5 w-5 text-gray-400" />
          <label htmlFor="status-filter" className="sr-only">Filter by Status</label>
          <select
            id="status-filter"
            className="form-select block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
          >
            <option value="all">All Statuses</option>
            {Object.keys(statusColors).map(status => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>

          <label htmlFor="parent-filter" className="sr-only">Filter by Parent</label>
          <select
            id="parent-filter"
            className="form-select block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            value={selectedParent}
            onChange={(e) => setSelectedParent(e.target.value)}
          >
            <option value="all">All Parents</option>
            <option value="root">Root Requirements</option>
            {Object.keys(analytics?.parentGroups || {}).map(key => (
              key !== 'Root Requirements' && <option key={key} value={key}>{analytics.parentGroups[key].name}</option>
            ))}
          </select>
        </div>

        {/* Render active view based on state */}
        {activeView === 'overview' && renderOverview()}
        {activeView === 'hierarchy' && renderHierarchy()}
        {activeView === 'details' && renderDetailsTable()}

      </div>
    </div>
  );
};

export default Dashboard;
