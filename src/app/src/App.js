import React, { useState, useEffect } from 'react';
import { getTodos, createTodo } from './api';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await getTodos();
      setTodos(response.data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const handleInputChange = (event) => {
    setNewTodo(event.target.value);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      await createTodo({ description: newTodo });
      setNewTodo('');
      fetchTodos();
    } catch (error) {
      console.error('Error creating todo:', error);
    }
  };

  return (
    <div className="App">
      <div>
        <h1>List of TODOs</h1>
        <ul>
          {todos.length > 0 ? (
            todos.map((todo) => <li key={todo._id}>{todo.description}</li>)
          ) : (
            <>
              <li>Learn Docker</li>
              <li>Learn React</li>
            </>
          )}
        </ul>
      </div>
      <div>
        <h1>Create a ToDo</h1>
        <form onSubmit={handleFormSubmit}>
          <div>
            <label htmlFor="todo">ToDo: </label>
            <input type="text" value={newTodo} onChange={handleInputChange} />
          </div>
          <div style={{ marginTop: '5px' }}>
            <button type="submit">Add ToDo!</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
