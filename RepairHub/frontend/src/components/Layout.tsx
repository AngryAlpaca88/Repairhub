import { Outlet, Link } from 'react-router-dom'

export default function Layout() {
  return (
    <div className="flex h-screen bg-background text-foreground">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-card">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-primary">RepairHub</h1>
        </div>
        <nav className="px-4 space-y-2">
          <Link to="/" className="block px-4 py-2 rounded hover:bg-accent hover:text-accent-foreground">
            Dashboard
          </Link>
          <Link to="/tickets" className="block px-4 py-2 rounded hover:bg-accent hover:text-accent-foreground">
            Tickets
          </Link>
          <Link to="/customers" className="block px-4 py-2 rounded hover:bg-accent hover:text-accent-foreground">
            Customers
          </Link>
          <Link to="/inventory" className="block px-4 py-2 rounded hover:bg-accent hover:text-accent-foreground">
            Inventory
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <header className="h-16 border-b flex items-center px-6 justify-between">
          <h2 className="text-lg font-semibold">Location: Computer Corner HQ</h2>
          <div className="flex items-center gap-4">
            <span>User Profile</span>
          </div>
        </header>
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
