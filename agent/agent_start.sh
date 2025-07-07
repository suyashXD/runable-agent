#!/bin/bash

# Activate the context manager
python3 context_manager.py init

# Simulate task execution (React Todo App)
echo "Starting task: $TASK"

npx create-react-app todo-app
cd todo-app

cat > src/Todo.js <<EOL
import React, { useState } from 'react';

function Todo() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    if (input) {
      setTodos([...todos, input]);
      setInput('');
    }
  };

  return (
    <div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map((todo, idx) => (
          <li key={idx}>{todo}</li>
        ))}
      </ul>
    </div>
  );
}

export default Todo;
EOL

cat > src/App.js <<EOL
import React from 'react';
import Todo from './Todo';
import './App.css';

function App() {
  return (
    <div className="App">
      <Todo />
    </div>
  );
}

export default App;
EOL

# Log task completion
echo "Task completed: Created a todo app in React" | python3 context_manager.py append

# Mark as done
touch /workspace/DONE
