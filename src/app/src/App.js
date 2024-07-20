import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [todos, setTodos] = useState(null); // Initialize as null
  const [newTodo, setNewTodo] = useState('');

  useEffect(() => {
    // Fetch TODOs from the backend when the component mounts
    axios.get('http://localhost:8000/todos/')
      .then(response => {
        setTodos(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the TODOs!', error);
      });
  }, []);

  const handleInputChange = (event) => {
    setNewTodo(event.target.value);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    // Post new TODO to the backend
    axios.post('http://localhost:8000/todos/', { description: newTodo })
      .then(response => {
        setTodos(response.data); // Update the TODOs list
        setNewTodo(''); // Clear the input field
      })
      .catch(error => {
        console.error('There was an error creating the TODO!', error);
      });
  };

  return (
    <div className="App">
      <div>
        <h1>List of TODOs</h1>
        <ul>
          {todos && todos.length > 0 ? (
            todos.map((todo) => (
              <li key={todo._id}>{todo.description}</li>
            ))
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
