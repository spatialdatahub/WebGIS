import React from 'react';
import ReactDOM from 'react-dom';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';

// import containers
import SearchBar from './reactify_src/containers/Sidebar/Searchbar';
import ClearMapButton from './reactify_src/containers/Sidebar/ClearMapButton';
import SidebarDatasetList from './reactify_src/containers/Sidebar/SidebarDatasetList';
import MapContainer from './reactify_src/containers/MapContainer/MapContainer';




const App = props => {

    // to be put through the MapContainer container
    const initialMapState = {
        lat: 51.505,
        lng: -0.09,
        zoom: 13
    };

    return (
        <div className='row' id='main'>
          <MapContainer mapState={initialMapState} />
          <div
            className='col-xs-12 col-md-4 col-lg-3'
            id='datasetsContainer'>

            <ul className='nav nav-pills nav-stacked' id='searchBarClearMapUl'>
              <SearchBar />
              <ClearMapButton />
            </ul>  

            <SidebarDatasetList datasetList={props.datasetList} />
          </div>
        </div>
    );
};


ReactDOM.render(
    <App datasetList={window.json_data} />,
    window.react_mount
);
