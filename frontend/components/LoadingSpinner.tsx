export default function LoadingSpinner() {
  return (
    <div className="mt-8 flex flex-col items-center justify-center py-12">
      <div className="relative">
        {/* Outer spinning ring */}
        <div className="w-16 h-16 border-4 border-blue-200 dark:border-blue-800 rounded-full animate-pulse"></div>
        {/* Inner spinning ring */}
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-blue-600 dark:border-t-blue-400 rounded-full animate-spin"></div>
      </div>
      <p className="mt-4 text-gray-600 dark:text-gray-300 font-medium">
        기사를 스크래핑하고 있습니다...
      </p>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
        잠시만 기다려주세요
      </p>
    </div>
  )
}
