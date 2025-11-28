import { useCurrentUser } from '../hooks/useCurrentUser';

function Dashboard() {
  const { user } = useCurrentUser();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm font-medium">Open Tickets</h3>
          <p className="text-3xl font-bold text-blue-600">--</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm font-medium">In Progress</h3>
          <p className="text-3xl font-bold text-yellow-600">--</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm font-medium">Completed Today</h3>
          <p className="text-3xl font-bold text-green-600">--</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Welcome, {user?.full_name}!</h2>
        <p className="text-gray-600 mb-4">
          This is your RepairHub dashboard. Use the navigation above to manage tickets,
          customers, and inventory.
        </p>
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4">
          <p className="text-blue-700">
            <strong>Quick tip:</strong> Create a new repair ticket by clicking &quot;New Ticket&quot;
            in the navigation bar.
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-3">Recent Tickets</h3>
          <p className="text-gray-500 text-sm">No recent tickets to display.</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-3">Low Stock Alerts</h3>
          <p className="text-gray-500 text-sm">No low stock items.</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
