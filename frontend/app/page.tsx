'use client'

import { useState } from 'react'
import ArticleForm from '@/components/ArticleForm'
import ArticleResult from '@/components/ArticleResult'
import LoadingSpinner from '@/components/LoadingSpinner'
import EvaluationResult from '@/components/EvaluationResult'

export interface Article {
  title: string
  author: string
  press: string
  published_at: string
  body: string
  original_url: string
}

export interface Evaluation {
  evaluation_summary: string
  scores: {
    [key: string]: number
  }
  detailed_feedback?: string
}

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [evaluating, setEvaluating] = useState(false)
  const [article, setArticle] = useState<Article | null>(null)
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleScrape = async (url: string) => {
    setLoading(true)
    setError(null)
    setArticle(null)
    setEvaluation(null)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

      // Step 1: 스크래핑
      const scrapeResponse = await fetch(`${apiUrl}/scrape`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      })

      if (!scrapeResponse.ok) {
        const errorData = await scrapeResponse.json()
        throw new Error(errorData.detail?.error || '스크래핑에 실패했습니다')
      }

      const articleData: Article = await scrapeResponse.json()
      setArticle(articleData)
      setLoading(false)

      // Step 2: 평가 (스크래핑 성공 후 자동 호출)
      setEvaluating(true)

      const evaluateResponse = await fetch(`${apiUrl}/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          article_body: articleData.body,
          article_title: articleData.title,
        }),
      })

      if (!evaluateResponse.ok) {
        const errorData = await evaluateResponse.json()
        console.error('평가 실패:', errorData)
        // 평가 실패해도 스크래핑 결과는 유지
      } else {
        const evaluationData: Evaluation = await evaluateResponse.json()
        setEvaluation(evaluationData)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다')
    } finally {
      setLoading(false)
      setEvaluating(false)
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
        <ArticleForm onSubmit={handleScrape} disabled={loading || evaluating} />

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

        {/* Loading Spinner - Scraping */}
        {loading && (
          <div className="mt-8 flex flex-col items-center justify-center py-12">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-blue-200 dark:border-blue-800 rounded-full animate-pulse"></div>
              <div className="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-blue-600 dark:border-t-blue-400 rounded-full animate-spin"></div>
            </div>
            <p className="mt-4 text-gray-600 dark:text-gray-300 font-medium">
              기사를 스크래핑하고 있습니다...
            </p>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              잠시만 기다려주세요
            </p>
          </div>
        )}

        {/* Loading Spinner - Evaluating */}
        {evaluating && !loading && (
          <div className="mt-8 flex flex-col items-center justify-center py-12">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-purple-200 dark:border-purple-800 rounded-full animate-pulse"></div>
              <div className="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-purple-600 dark:border-t-purple-400 rounded-full animate-spin"></div>
            </div>
            <p className="mt-4 text-gray-600 dark:text-gray-300 font-medium">
              AI가 기사를 평가하고 있습니다...
            </p>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              8차원 평가 기준을 적용 중입니다
            </p>
          </div>
        )}

        {/* Article Result */}
        {article && !loading && <ArticleResult article={article} />}

        {/* Evaluation Result */}
        {evaluation && !evaluating && <EvaluationResult evaluation={evaluation} />}
      </div>
    </main>
  )
}
