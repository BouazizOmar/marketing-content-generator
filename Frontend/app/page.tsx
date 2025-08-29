"use client"

import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import { Header } from "@/components/header"
import { ContentGenerator } from "@/components/content-generator"
import { TrendsViewer } from "@/components/trends-viewer"
import { SentimentAnalyzer } from "@/components/sentiment-analyzer"
import { Toaster } from "@/components/ui/toaster"

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-8 pt-24">
          <Routes>
            <Route path="/" element={<Navigate to="/generate" replace />} />
            <Route path="/generate" element={<ContentGenerator />} />
            <Route path="/trends" element={<TrendsViewer />} />
            <Route path="/analyze" element={<SentimentAnalyzer />} />
          </Routes>
        </main>
        <footer className="border-t bg-background py-6 text-center text-sm text-muted-foreground">
          © 2025 ContentGen AI
        </footer>
        <Toaster />
      </div>
    </Router>
  )
}
