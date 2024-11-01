import { Link } from "react-router-dom";
import { EventSamples } from "./Samples";

const EventList = () => {
    return (
        <div className="event-list-section">
            {EventSamples.map((item, index) => (
                <div className="event-block" key={index}>
                    <div className="event-img-block">
                        <img className="event-img" alt="event-img"/>
                    </div>
                    <div className="event-text-block">
                        <div className="event-title">{item.name} - {item.organization}</div>
                        <div className="event-type">{item.type}</div>
                        <div className="event-date">{item.day}</div>
                        <div className="event-location">{item.location}</div>
                    </div>
                    <div className="event-button-block">
                        <Link to={item.websitelink} style={{ maxWidth: 'fit-content' }} target="_blank">
                            <button className="event-button">REGISTER NOW</button>
                        </Link>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default EventList;
