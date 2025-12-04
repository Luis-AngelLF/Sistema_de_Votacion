import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-center text-blue-600 mb-6">
          Sistema de Votación
        </h1>
        <div className="space-y-4">
          <button 
            onClick={() => setCount((count) => count + 1)}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition duration-200"
          >
            Contador: {count}
          </button>
          <p className="text-center text-gray-600">
            Tailwind CSS está funcionando correctamente ✓
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
