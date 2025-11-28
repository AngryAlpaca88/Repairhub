import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api';

interface Ticket {
  id: number;
  ticket_number: string;
  status: string;
  priority: string;
  device_type: string | null;
  device_brand: string | null;
  device_model: string | null;
  issue_description: string;
  total_price: string;
  created_at: string;
  customer?: {
    first_name: string;
    last_name: string;
  };
}

function Tickets() {
  const [statusFilter, setStatusFilter] = useState<string>('');

  const { data: tickets, isLoading, error } = useQuery<Ticket[]>({
    queryKey: ['tickets', statusFilter],
    queryFn: () => api.get('/tickets', { status: statusFilter || undefined }),
  });

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      intake: 'bg-gray-100 text-gray-800',
      diagnosing: 'bg-blue-100 text-blue-800',
      waiting_parts: 'bg-yellow-100 text-yellow-800',
      in_progress: 'bg-purple-100 text-purple-800',
      ready: 'bg-green-100 text-green-800',
      completed: 'bg-green-200 text-green-900',
      cancelled: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      low: 'text-gray-500',
      normal: 'text-blue-500',
      high: 'text-orange-500',
      urgent: 'text-red-600 font-bold',
    };
    return colors[priority] || 'text-gray-500';
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Tickets</h1>
        <a
          href="/tickets/new"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + New Ticket
        </a>
      </div>

      <div className="bg-white rounded-lg shadow mb-6 p-4">
        <div className="flex gap-4 items-center">
          <label className="text-sm font-medium text-gray-700">Filter by status:</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="">All</option>
            <option value="intake">Intake</option>
            <option value="diagnosing">Diagnosing</option>
            <option value="waiting_parts">Waiting for Parts</option>
            <option value="in_progress">In Progress</option>
            <option value="ready">Ready for Pickup</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {isLoading && (
        <div className="text-center py-8 text-gray-500">Loading tickets...</div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded">
          Error loading tickets. Please try again.
        </div>
      )}

      {tickets && tickets.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No tickets found. Create your first ticket to get started!
        </div>
      )}

      {tickets && tickets.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ticket #
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Device
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Priority
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tickets.map((ticket) => (
                <tr key={ticket.id} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                    {ticket.ticket_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {ticket.customer
                      ? `${ticket.customer.first_name} ${ticket.customer.last_name}`
                      : '--'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {[ticket.device_brand, ticket.device_model].filter(Boolean).join(' ') ||
                      ticket.device_type ||
                      '--'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                        ticket.status
                      )}`}
                    >
                      {ticket.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm ${getPriorityColor(ticket.priority)}`}>
                    {ticket.priority}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${parseFloat(ticket.total_price).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Tickets;
