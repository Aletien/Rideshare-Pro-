'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const userData = localStorage.getItem('user')
    if (!userData) {
      router.push('/login')
      return
    }
    setUser(JSON.parse(userData))
    setLoading(false)
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    router.push('/')
  }

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">RideShare Pro</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">{user?.first_name} {user?.last_name}</span>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <h2 className="text-3xl font-bold mb-6">Welcome, {user?.first_name}!</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {user?.user_type === 'passenger' && (
              <>
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">Request a Ride</h3>
                  <p className="text-gray-600 mb-4">Book a ride to your destination</p>
                  <Link href="/rides/request" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    Request Ride
                  </Link>
                </div>

                <div className="bg-green-50 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">My Rides</h3>
                  <p className="text-gray-600 mb-4">View your ride history</p>
                  <Link href="/rides/history" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
                    View Rides
                  </Link>
                </div>

                <div className="bg-purple-50 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">Profile</h3>
                  <p className="text-gray-600 mb-4">Manage your profile</p>
                  <Link href="/profile" className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
                    Edit Profile
                  </Link>
                </div>
              </>
            )}

            {user?.user_type === 'driver' && (
              <>
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">Go Online</h3>
                  <p className="text-gray-600 mb-4">Start accepting rides</p>
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    Go Online
                  </button>
                </div>

                <div className="bg-green-50 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">Earnings</h3>
                  <p className="text-gray-600 mb-4">View your earnings</p>
                  <Link href="/earnings" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
                    View Earnings
                  </Link>
                </div>

                <div className="bg-purple-50 p-6 rounded-lg">
                  <h3 className="text-xl font-bold mb-4">Profile</h3>
                  <p className="text-gray-600 mb-4">Manage your profile</p>
                  <Link href="/profile" className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
                    Edit Profile
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
