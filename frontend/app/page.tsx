'use client'

import { useState } from 'react'
import ArticleForm from '@/components/ArticleForm'
import ArticleResult from '@/components/ArticleResult'
import LoadingSpinner from '@/components/LoadingSpinner'

export interface Article {
  title: string
  author: string
  press: string
  published_at: string
  body: string
  original_url: string
}

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [article, setArticle] = useState<Article | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleScrape = async (url: string) => {
    setLoading(true)
    setError(null)
    setArticle(null)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/scrape`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail?.error || '스크래핑에 실패했습니다')
      }

      const data: Article = await response.json()
      setArticle(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
            CR Template Hub
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            한국 주요 언론사 기사 평가 플랫폼
          </p>
          <div className="mt-4 flex justify-center gap-2 flex-wrap">
            <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-3 py-1 rounded-full">
              네이버 뉴스
            </span>
            <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-3 py-1 rounded-full">
              다음 뉴스
            </span>
            <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-3 py-1 rounded-full">
              연합뉴스
            </span>
            <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-3 py-1 rounded-full">
              조선일보
            </span>
            <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-3 py-1 rounded-full">
              중앙일보
            </span>
            <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-3 py-1 rounded-full">
              한겨레
            </span>
            <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-3 py-1 rounded-full">
              한국경제
            </span>
          </div>
        </div>

        {/* Article Form */}
        <ArticleForm onSubmit={handleScrape} disabled={loading} />

        {/* Error Message */}
        {error && (
          <div className="mt-6 max-w-4xl mx-auto">
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-red-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                    오류 발생
                  </h3>
                  <div className="mt-2 text-sm text-red-700 dark:text-red-300">
                    {error}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && <LoadingSpinner />}

        {/* Article Result */}
        {article && !loading && <ArticleResult article={article} />}
      </div>
    </main>
  )
}
