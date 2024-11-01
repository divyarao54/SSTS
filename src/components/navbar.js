import { NavLink } from 'react-router-dom';
import './styles/navbar.css';

const NavBar = () =>{
    return(
        <div className="navbar-section">
            <div className="navbar-logo">SSTS</div>
            <div className="navbar-components">
                <div className="navbar-route">
                    <NavLink className={({isActive}) => isActive? 'nav-link-active' : 'nav-link'} to='/home'>Home</NavLink>
                </div>
                <div className="navbar-route">
                    <NavLink className={({isActive}) => isActive? 'nav-link-active' : 'nav-link'} to='/events'>Events</NavLink>
                </div>
                <div className="navbar-route">
                    <NavLink className={({isActive}) => isActive? 'nav-link-active' : 'nav-link'} to='/courses'>Courses</NavLink>
                </div>
                <div className="navbar-route">
                    <NavLink className={({isActive}) => isActive? 'nav-link-active' : 'nav-link'} to='/profile'>My Profile</NavLink>
                </div>
            </div>
        </div>
    );
}

export default NavBar;