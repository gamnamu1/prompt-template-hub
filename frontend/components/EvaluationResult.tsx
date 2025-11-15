interface EvaluationResultProps {
  evaluation: {
    evaluation_summary: string
    scores: {
      [key: string]: number
    }
    detailed_feedback?: string
  }
}

export default function EvaluationResult({ evaluation }: EvaluationResultProps) {
  // 8차원 평가 기준 (순서 고정)
  const dimensions = [
    { key: '진실성', label: '진실성 (Truth)', color: 'bg-blue-500' },
    { key: '정확성', label: '정확성 (Accuracy)', color: 'bg-green-500' },
    { key: '공정성', label: '공정성 (Fairness)', color: 'bg-yellow-500' },
    { key: '투명성', label: '투명성 (Transparency)', color: 'bg-purple-500' },
    { key: '맥락', label: '맥락 (Context)', color: 'bg-pink-500' },
    { key: '인권_존중', label: '인권 존중 (Human Rights)', color: 'bg-red-500' },
    { key: '책임성', label: '책임성 (Accountability)', color: 'bg-indigo-500' },
    { key: '독립성', label: '독립성 (Independence)', color: 'bg-teal-500' },
  ]

  // 평균 점수 계산
  const scores = Object.values(evaluation.scores)
  const averageScore = scores.length > 0
    ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1)
    : '0'

  return (
    <div className="mt-8 max-w-6xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-700 dark:to-purple-700 px-8 py-6">
          <h2 className="text-2xl font-bold text-white mb-2">
            AI 기사 평가 결과
          </h2>
          <p className="text-indigo-100">
            저널리즘 윤리 기준 8차원 분석
          </p>
        </div>

        {/* Content */}
        <div className="p-8 space-y-8">
          {/* Average Score */}
          <div className="text-center pb-6 border-b border-gray-200 dark:border-gray-700">
            <div className="inline-flex items-baseline gap-2">
              <span className="text-6xl font-bold text-indigo-600 dark:text-indigo-400">
                {averageScore}
              </span>
              <span className="text-2xl text-gray-500 dark:text-gray-400">/ 10</span>
            </div>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              종합 평균 점수
            </p>
          </div>

          {/* Evaluation Summary */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              평가 요약
            </h3>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed bg-gray-50 dark:bg-slate-700/50 p-4 rounded-lg">
              {evaluation.evaluation_summary}
            </p>
          </div>

          {/* Scores */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              8차원 평가 점수
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {dimensions.map((dim) => {
                const score = evaluation.scores[dim.key] || 0
                const percentage = (score / 10) * 100

                return (
                  <div
                    key={dim.key}
                    className="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-4"
                  >
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {dim.label}
                      </span>
                      <span className="text-lg font-bold text-gray-900 dark:text-white">
                        {score}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2.5">
                      <div
                        className={`${dim.color} h-2.5 rounded-full transition-all duration-500`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Detailed Feedback */}
          {evaluation.detailed_feedback && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                상세 피드백
              </h3>
              <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <svg
                      className="h-5 w-5 text-amber-400"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-amber-800 dark:text-amber-200 whitespace-pre-wrap">
                      {evaluation.detailed_feedback}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Legend */}
          <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
            <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
              * 평가는 Claude AI (Sonnet 4)를 사용하여 수행되었습니다
              <br />
              ** 각 차원은 1-10점 척도로 평가됩니다 (10점이 가장 우수)
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
