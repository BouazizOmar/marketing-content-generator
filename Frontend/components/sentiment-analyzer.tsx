"use client"

import { useState } from "react"
import { Loader2, BarChart3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/hooks/use-toast"
import { analysisApi } from "@/lib/api"
import { cn } from "@/lib/utils"

export function SentimentAnalyzer() {
  const [content, setContent] = useState("")
  const [sentiment, setSentiment] = useState<number | null>(null)
  const [sentimentLabel, setSentimentLabel] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleAnalyze = async () => {
    if (!content.trim()) {
      toast({
        title: "Content required",
        description: "Please enter content to analyze",
        variant: "destructive",
      })
      return
    }

    setIsLoading(true)
    try {
      const response = await analysisApi.analyze(content)
      setSentiment(response.sentiment)
      setSentimentLabel(response.sentiment_label)

      toast({
        title: "Analysis complete",
        description: `Content sentiment: ${response.sentiment_label}`,
      })
    } catch (error) {
      console.error("[v0] Sentiment analysis error:", error)
      toast({
        title: "Analysis failed",
        description: "Failed to analyze sentiment. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getSentimentColor = (label: string | null) => {
    switch (label) {
      case "positive":
        return "bg-green-500 text-white"
      case "negative":
        return "bg-red-500 text-white"
      case "neutral":
        return "bg-gray-500 text-white"
      default:
        return "bg-gray-500 text-white"
    }
  }

  const getSentimentProgress = (score: number | null) => {
    if (score === null) return 50
    return ((score + 1) / 2) * 100
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-balance">Sentiment Analyzer</h1>
        <p className="text-muted-foreground mt-2">Analyze the emotional tone of your marketing content</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Content to Analyze</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Enter your content</label>
              <Textarea
                placeholder="e.g., Boost your fitness with our amazing new app!"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="min-h-[150px]"
              />
            </div>

            <Button onClick={handleAnalyze} disabled={isLoading} className="w-full hover:bg-blue-600">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <BarChart3 className="mr-2 h-4 w-4" />
                  Analyze
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center justify-center h-40">
                <Loader2 className="h-8 w-8 animate-spin" />
              </div>
            ) : sentiment !== null && sentimentLabel ? (
              <div className="space-y-6">
                <div className="text-center">
                  <Badge className={cn("text-lg px-4 py-2", getSentimentColor(sentimentLabel))}>
                    {sentimentLabel.charAt(0).toUpperCase() + sentimentLabel.slice(1)}
                  </Badge>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Sentiment Score</span>
                    <span className="font-mono">{sentiment.toFixed(3)}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3 dark:bg-gray-700">
                    <div
                      className={cn(
                        "h-3 rounded-full transition-all duration-500",
                        sentimentLabel === "positive"
                          ? "bg-green-500"
                          : sentimentLabel === "negative"
                            ? "bg-red-500"
                            : "bg-gray-500",
                      )}
                      style={{ width: `${getSentimentProgress(sentiment)}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Negative (-1)</span>
                    <span>Neutral (0)</span>
                    <span>Positive (+1)</span>
                  </div>
                </div>

                <div className="p-4 bg-muted rounded-lg">
                  <p className="text-sm">
                    <strong>Interpretation:</strong> Your content has a{" "}
                    <span
                      className={cn(
                        "font-semibold",
                        sentimentLabel === "positive"
                          ? "text-green-600 dark:text-green-400"
                          : sentimentLabel === "negative"
                            ? "text-red-600 dark:text-red-400"
                            : "text-gray-600 dark:text-gray-400",
                      )}
                    >
                      {sentimentLabel}
                    </span>{" "}
                    emotional tone with a score of {sentiment.toFixed(3)}.
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center text-muted-foreground py-8">
                <BarChart3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Analysis results will appear here</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
