import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CR Template Hub - 기사 평가 플랫폼',
  description: '한국 주요 언론사 기사를 스크래핑하고 저널리즘 윤리 기준으로 평가하는 플랫폼',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
