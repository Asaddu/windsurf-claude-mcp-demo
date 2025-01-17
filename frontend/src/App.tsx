import { useState, useEffect, useCallback } from 'react'
import Editor from '@monaco-editor/react'
import { BeakerIcon, FireIcon, SparklesIcon, LightBulbIcon, BookOpenIcon } from '@heroicons/react/24/solid'

interface Challenge {
  id: number
  title: string
  description: string
  template: string
  level: string
  xp: number
  hints: string[]
  example: string
  explanation: string
}

interface Achievement {
  name: string
  xp: number
}

function App() {
  const [challenges, setChallenges] = useState<Challenge[]>([])
  const [currentChallenge, setCurrentChallenge] = useState<Challenge | null>(null)
  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [xp, setXp] = useState(0)
  const [achievements, setAchievements] = useState<Achievement[]>([])
  const [showAchievement, setShowAchievement] = useState(false)
  const [latestAchievement, setLatestAchievement] = useState<Achievement | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [showHints, setShowHints] = useState(false)
  const [currentHintIndex, setCurrentHintIndex] = useState(0)
  const [showExample, setShowExample] = useState(false)

  useEffect(() => {
    fetch('http://localhost:8000/challenges')
      .then(res => res.json())
      .then(data => {
        setChallenges(data)
        if (data.length > 0) {
          setCurrentChallenge(data[0])
          setCode(data[0].template)
        }
      })

    const websocket = new WebSocket('ws://localhost:8000/ws')
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'result') {
        setIsRunning(false)
        setOutput(data.output)
        setXp(data.totalXp)
        
        if (data.rewards && data.rewards.length > 0) {
          const newAchievement = data.rewards[data.rewards.length - 1]
          setLatestAchievement(newAchievement)
          setShowAchievement(true)
          setTimeout(() => setShowAchievement(false), 3000)
          setAchievements(prev => [...prev, ...data.rewards])
        }
      } else if (data.type === 'hint_reward') {
        setXp(data.totalXp)
        setAchievements(prev => [...prev, data.achievement])
      }
    }
    setWs(websocket)

    return () => {
      websocket.close()
    }
  }, [])

  const handleRunCode = useCallback(() => {
    if (ws && ws.readyState === WebSocket.OPEN && currentChallenge) {
      setIsRunning(true)
      ws.send(JSON.stringify({
        type: 'code_submission',
        code: code,
        challengeId: currentChallenge.id
      }))
    }
  }, [ws, code, currentChallenge])

  const handleRequestHint = useCallback(() => {
    if (ws && ws.readyState === WebSocket.OPEN && currentChallenge) {
      ws.send(JSON.stringify({
        type: 'request_hint',
        challengeId: currentChallenge.id
      }))
    }
  }, [ws, currentChallenge])

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      handleRunCode()
    }
  }, [handleRunCode])

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [handleKeyDown])

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      {/* Achievement Popup */}
      {showAchievement && latestAchievement && (
        <div className="fixed top-4 right-4 bg-yellow-500 text-black p-4 rounded-lg shadow-lg transform transition-transform animate-bounce z-50">
          <div className="flex items-center gap-2">
            <SparklesIcon className="h-6 w-6" />
            <div>
              <h3 className="font-bold">Achievement Unlocked!</h3>
              <p>{latestAchievement.name} (+{latestAchievement.xp} XP)</p>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="bg-gray-800 shadow-lg border-b border-gray-700 sticky top-0 z-40">
        <div className="w-full mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl md:text-3xl font-bold flex items-center gap-2">
              <BeakerIcon className="h-8 w-8 text-purple-500" />
              Code Quest
            </h1>
            <div className="flex items-center gap-4">
              <div className="bg-gray-700 px-4 py-2 rounded-lg flex items-center gap-2">
                <FireIcon className="h-6 w-6 text-yellow-500" />
                <span className="font-bold">{xp} XP</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="w-full mx-auto">
        {/* Challenge Selection */}
        <div className="px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
            {challenges.map(challenge => (
              <button
                key={challenge.id}
                onClick={() => {
                  setCurrentChallenge(challenge)
                  setCode(challenge.template)
                  setShowHints(false)
                  setCurrentHintIndex(0)
                  setShowExample(false)
                }}
                className={`flex-shrink-0 px-4 py-2 rounded-lg ${
                  currentChallenge?.id === challenge.id
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-700 hover:bg-gray-600'
                } transition-colors`}
              >
                {challenge.title}
              </button>
            ))}
          </div>
        </div>

        {currentChallenge && (
          <div className="space-y-6 px-4 sm:px-6 lg:px-8">
            {/* Challenge Info */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-4">
                <div className="flex-1">
                  <h2 className="text-xl font-semibold mb-2">{currentChallenge.title}</h2>
                  <p className="text-gray-300 mb-2">{currentChallenge.description}</p>
                  <div className="flex gap-2">
                    <span className="bg-purple-600 px-2 py-1 rounded text-sm">
                      {currentChallenge.level}
                    </span>
                    <span className="bg-yellow-600 px-2 py-1 rounded text-sm">
                      {currentChallenge.xp} XP
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      handleRequestHint()
                      setShowHints(!showHints)
                    }}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg flex items-center gap-2"
                  >
                    <LightBulbIcon className="h-5 w-5" />
                    Hints
                  </button>
                  <button
                    onClick={() => setShowExample(!showExample)}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg flex items-center gap-2"
                  >
                    <BookOpenIcon className="h-5 w-5" />
                    Example
                  </button>
                </div>
              </div>
            </div>

            {/* Hints Panel */}
            {showHints && (
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <LightBulbIcon className="h-5 w-5 text-yellow-500" />
                  Helpful Hints
                </h3>
                <div className="space-y-4">
                  {currentChallenge.hints.map((hint, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg ${
                        index <= currentHintIndex
                          ? 'bg-gray-700'
                          : 'bg-gray-900 opacity-50'
                      }`}
                    >
                      {index <= currentHintIndex ? (
                        <p>{hint}</p>
                      ) : (
                        <button
                          onClick={() => setCurrentHintIndex(index)}
                          className="text-blue-400 hover:text-blue-300"
                        >
                          Reveal next hint
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Example Panel */}
            {showExample && (
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <BookOpenIcon className="h-5 w-5 text-green-500" />
                  Example Solution
                </h3>
                <div className="space-y-4">
                  <div className="bg-gray-900 p-4 rounded-lg font-mono text-sm">
                    {currentChallenge.example}
                  </div>
                  <div className="bg-gray-700 p-4 rounded-lg">
                    <h4 className="font-semibold mb-2">Explanation:</h4>
                    <p>{currentChallenge.explanation}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Code Editor and Output */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">Code Editor</h3>
                  <button
                    onClick={handleRunCode}
                    disabled={isRunning}
                    className={`px-4 py-2 ${
                      isRunning
                        ? 'bg-gray-600 cursor-not-allowed'
                        : 'bg-purple-600 hover:bg-purple-700'
                    } text-white rounded transition-colors flex items-center gap-2`}
                  >
                    {isRunning ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                        Running...
                      </>
                    ) : (
                      <>Run Code (⌘/Ctrl + Enter)</>
                    )}
                  </button>
                </div>
                <div className="h-[400px] border border-gray-700 rounded-lg overflow-hidden">
                  <Editor
                    height="100%"
                    defaultLanguage="python"
                    theme="vs-dark"
                    value={code}
                    onChange={(value) => setCode(value || '')}
                    options={{
                      minimap: { enabled: false },
                      fontSize: 14,
                      quickSuggestions: true,
                      suggestOnTriggerCharacters: true,
                      parameterHints: { enabled: true },
                      tabSize: 4,
                      folding: true,
                    }}
                  />
                </div>
              </div>

              <div className="space-y-6">
                <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                  <h3 className="text-lg font-semibold mb-4">Output</h3>
                  <div className="h-[200px] bg-gray-900 rounded-lg p-4 font-mono text-sm overflow-auto">
                    {output || 'Your code output will appear here...'}
                  </div>
                </div>

                <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                  <h3 className="text-lg font-semibold mb-4">Achievements</h3>
                  {achievements.length === 0 ? (
                    <p className="text-gray-400">Complete challenges to earn achievements!</p>
                  ) : (
                    <div className="space-y-2">
                      {achievements.map((achievement, index) => (
                        <div
                          key={index}
                          className="flex items-center gap-2 bg-gray-700 p-2 rounded"
                        >
                          <SparklesIcon className="h-5 w-5 text-yellow-500" />
                          <span>{achievement.name}</span>
                          <span className="text-yellow-500">+{achievement.xp} XP</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
