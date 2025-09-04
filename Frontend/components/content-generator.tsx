"use client"

import type React from "react"
import { useState, useCallback } from "react"
import { Upload, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { contentApi } from "@/lib/api"

export function ContentGenerator() {
  const [prompt, setPrompt] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const [generatedContent, setGeneratedContent] = useState("")
  const [imageUrl, setImageUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleFileUpload = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = event.target.files?.[0]
      if (selectedFile) {
        if (selectedFile.size > 5 * 1024 * 1024) {
          toast({
            title: "File too large",
            description: "Please select a file smaller than 5MB",
            variant: "destructive",
          })
          return
        }

        const allowedTypes = ["text/csv", "application/pdf", "application/vnd.ms-excel"]
        if (!allowedTypes.includes(selectedFile.type)) {
          toast({
            title: "Invalid file type",
            description: "Please select a CSV or PDF file",
            variant: "destructive",
          })
          return
        }

        setFile(selectedFile)
      }
    },
    [toast],
  )

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast({
        title: "Prompt required",
        description: "Please enter a prompt to generate content",
        variant: "destructive",
      })
      return
    }

    setIsLoading(true)
    try {
      const fileData = file ? await fileToBase64(file) : undefined
      const response = await contentApi.generate(prompt, fileData)
      setGeneratedContent(response.content)
      setImageUrl(response.image_url)

      toast({
        title: "Content generated successfully",
        description: "Your marketing content has been created",
      })
    } catch (error) {
      console.error("[v0] Content generation error:", error)
      const isNetworkError =
        error instanceof Error && (error.message === "Network Error" || error.message.includes("ECONNREFUSED"))
      toast({
        title: "Generation failed",
        description: isNetworkError
          ? "Cannot connect to backend. Make sure FastAPI server is running on localhost:8000"
          : "Failed to generate content. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result as string)
      reader.onerror = (error) => reject(error)
    })
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-balance">Content Generator</h1>
        <p className="text-muted-foreground mt-2">Generate engaging marketing content with AI assistance</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Input</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Prompt</label>
              <Textarea
                placeholder="e.g., Create a Twitter post for a fitness app"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="min-h-[100px]"
              />
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Upload File (Optional)</label>
              <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                <input type="file" accept=".csv,.pdf" onChange={handleFileUpload} className="hidden" id="file-upload" />
                <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center space-y-2">
                  <Upload className="h-8 w-8 text-muted-foreground" />
                  <span className="text-sm text-muted-foreground">
                    {file ? file.name : "Drop CSV/PDF files here or click to upload"}
                  </span>
                  <span className="text-xs text-muted-foreground">Max 5MB</span>
                </label>
              </div>
              {file && (
                <Button variant="outline" size="sm" onClick={() => setFile(null)} className="mt-2">
                  Remove file
                </Button>
              )}
            </div>

            <Button onClick={handleGenerate} disabled={isLoading} className="w-full hover:bg-blue-600">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                "Generate"
              )}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Generated Content</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center justify-center h-40">
                <Loader2 className="h-8 w-8 animate-spin" />
              </div>
            ) : generatedContent ? (
              <div className="space-y-4">
                <div className="p-4 bg-muted rounded-lg">
                  <p className="text-sm whitespace-pre-wrap">{generatedContent}</p>
                </div>
                {imageUrl && (
                  <img
                    src={imageUrl || "/placeholder.svg"}
                    alt="Generated content visual"
                    className="w-full max-w-[300px] h-[200px] object-cover rounded-lg"
                    onError={(e) => {
                      e.currentTarget.style.display = "none"
                    }}
                  />
                )}
              </div>
            ) : (
              <div className="text-center text-muted-foreground py-8">Generated content will appear here</div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
