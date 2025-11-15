import { Article } from '@/app/page'

interface ArticleResultProps {
  article: Article
}

export default function ArticleResult({ article }: ArticleResultProps) {
  return (
    <div className="mt-8 max-w-4xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 dark:from-blue-700 dark:to-blue-800 px-8 py-6">
          <h2 className="text-2xl font-bold text-white mb-2">
            스크래핑 결과
          </h2>
          <p className="text-blue-100">
            기사 정보를 성공적으로 가져왔습니다
          </p>
        </div>

        {/* Content */}
        <div className="p-8 space-y-6">
          {/* Metadata */}
          <div className="flex flex-wrap gap-3 pb-6 border-b border-gray-200 dark:border-gray-700">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
              <svg
                className="w-4 h-4 mr-1.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"
                />
              </svg>
              {article.press}
            </span>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
              <svg
                className="w-4 h-4 mr-1.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
              {article.author}
            </span>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
              <svg
                className="w-4 h-4 mr-1.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              {article.published_at}
            </span>
          </div>

          {/* Title */}
          <div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              제목
            </h3>
            <p className="text-lg text-gray-800 dark:text-gray-200 leading-relaxed">
              {article.title}
            </p>
          </div>

          {/* Body */}
          <div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
              본문
            </h3>
            <div className="prose prose-slate dark:prose-invert max-w-none">
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
                {article.body}
              </p>
            </div>
          </div>

          {/* Original URL */}
          <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
            <a
              href={article.original_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium transition-colors"
            >
              <svg
                className="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
              원본 기사 보기
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
