"use client"

import { useState, useEffect } from "react"
import { RefreshCw, Loader2, TrendingUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { trendsApi } from "@/lib/api"

export function TrendsViewer() {
  const [trends, setTrends] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const fetchTrends = async () => {
    setIsLoading(true)
    try {
      const response = await trendsApi.getTrends()
      setTrends(response.trends)
      toast({
        title: "Trends updated",
        description: `Loaded ${response.trends.length} marketing trends`,
      })
    } catch (error) {
      console.error("[v0] Trends fetch error:", error)
      toast({
        title: "Failed to fetch trends",
        description: "Unable to load marketing trends. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchTrends()
  }, [])

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-balance">Marketing Trends</h1>
        <p className="text-muted-foreground mt-2">Stay updated with the latest marketing trends and insights</p>
      </div>

      <div className="flex justify-center">
        <Button onClick={fetchTrends} disabled={isLoading} className="bg-green-500 hover:bg-green-600">
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Loading...
            </>
          ) : (
            <>
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh Trends
            </>
          )}
        </Button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-40">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      ) : trends.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {trends.map((trend, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center space-x-2 text-lg">
                  <TrendingUp className="h-5 w-5 text-green-500" />
                  <span className="text-balance">{trend}</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">Trending in marketing and content creation</p>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center text-muted-foreground py-8">
          <TrendingUp className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>No trends available. Click refresh to load trends.</p>
        </div>
      )}
    </div>
  )
}
