'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">RideShare Pro</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-700 hover:text-blue-600">
                Login
              </Link>
              <Link href="/register" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center text-white">
          <h2 className="text-5xl font-bold mb-6">Welcome to RideShare Pro</h2>
          <p className="text-xl mb-8">The modern ride-sharing platform built with Django & Next.js</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white text-gray-800 p-8 rounded-lg shadow-lg">
              <h3 className="text-2xl font-bold mb-4">🚗 For Passengers</h3>
              <p className="mb-6">Book rides easily and safely with our modern app</p>
              <Link href="/register?type=passenger" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
                Get Started
              </Link>
            </div>

            <div className="bg-white text-gray-800 p-8 rounded-lg shadow-lg">
              <h3 className="text-2xl font-bold mb-4">🚕 For Drivers</h3>
              <p className="mb-6">Earn money by providing rides on your schedule</p>
              <Link href="/register?type=driver" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
                Become a Driver
              </Link>
            </div>

            <div className="bg-white text-gray-800 p-8 rounded-lg shadow-lg">
              <h3 className="text-2xl font-bold mb-4">📊 Admin Dashboard</h3>
              <p className="mb-6">Manage the platform and view analytics</p>
              <Link href="/admin/login" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
                Admin Login
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
