export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-lg border bg-card text-card-foreground shadow-sm">
          <h3 className="font-semibold text-sm text-muted-foreground">Total Revenue (Today)</h3>
          <div className="text-2xl font-bold mt-2">$1,250.00</div>
        </div>
        <div className="p-6 rounded-lg border bg-card text-card-foreground shadow-sm">
          <h3 className="font-semibold text-sm text-muted-foreground">Open Tickets</h3>
          <div className="text-2xl font-bold mt-2">12</div>
        </div>
        <div className="p-6 rounded-lg border bg-card text-card-foreground shadow-sm">
          <h3 className="font-semibold text-sm text-muted-foreground">Low Stock Items</h3>
          <div className="text-2xl font-bold mt-2 text-destructive">3</div>
        </div>
      </div>
    </div>
  )
}
