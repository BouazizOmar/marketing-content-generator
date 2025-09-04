"use client"

import { useEffect, useState } from "react"
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import { Header } from "@/components/header"
import { ContentGenerator } from "@/components/content-generator"
import { Toaster } from "@/components/ui/toaster"

export default function App() {
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  if (!mounted) return null

  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-8 pt-24">
          <Routes>
            <Route path="/" element={<Navigate to="/generate" replace />} />
            <Route path="/generate" element={<ContentGenerator />} />
          </Routes>
        </main>
        <footer className="border-t border-t-border bg-background py-6 text-center text-sm text-muted-foreground">
          © 2025 ContentGen AI
        </footer>
        <Toaster />
      </div>
    </Router>
  )
}
