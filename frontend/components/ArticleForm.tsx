'use client'

import { useState, FormEvent } from 'react'

interface ArticleFormProps {
  onSubmit: (url: string) => void
  disabled?: boolean
}

export default function ArticleForm({ onSubmit, disabled = false }: ArticleFormProps) {
  const [url, setUrl] = useState('')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (url.trim()) {
      onSubmit(url.trim())
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="article-url"
              className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2"
            >
              기사 URL
            </label>
            <input
              id="article-url"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://n.news.naver.com/mnews/article/..."
              disabled={disabled}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-slate-700 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            />
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              지원 언론사: 네이버 뉴스, 다음 뉴스, 연합뉴스, 조선일보, 중앙일보, 한겨레, 한국경제
            </p>
          </div>

          <button
            type="submit"
            disabled={disabled || !url.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800"
          >
            {disabled ? '평가 중...' : '평가하기'}
          </button>
        </form>
      </div>
    </div>
  )
}
