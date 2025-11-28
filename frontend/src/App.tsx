import { Routes, Route, Navigate } from 'react-router-dom';
import { useCurrentUser } from './hooks/useCurrentUser';
import Dashboard from './pages/Dashboard';
import Tickets from './pages/Tickets';
import CreateTicket from './pages/CreateTicket';
import Login from './pages/Login';

function App() {
  const { user, isLoading } = useCurrentUser();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-lg text-gray-600">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <h1 className="text-xl font-bold">RepairHub</h1>
              <a href="/" className="hover:text-blue-200">Dashboard</a>
              <a href="/tickets" className="hover:text-blue-200">Tickets</a>
              <a href="/tickets/new" className="hover:text-blue-200">New Ticket</a>
            </div>
            <div className="flex items-center space-x-4">
              <span>{user.full_name}</span>
              <span className="text-sm bg-blue-500 px-2 py-1 rounded">{user.role}</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tickets" element={<Tickets />} />
          <Route path="/tickets/new" element={<CreateTicket />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
