import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import './App.css';
import LandingPage from './routes/landing';
import EventsPage from './routes/events';
import CoursesPage from './routes/courses';
import ProfilePage from './routes/profile';
import LoginPage from './routes/login';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Navigate to="/home"/>}/>
          <Route path='/home' element={<LandingPage/>}/>
          <Route path='/events' element={<EventsPage/>}/>
          <Route path='/courses' element={<CoursesPage/>}/>
          <Route path='/profile' element={<ProfilePage/>}/>
          <Route path= '/login' element={<LoginPage/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
