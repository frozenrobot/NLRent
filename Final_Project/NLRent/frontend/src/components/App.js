import React, { Component } from "react";
import { render } from "react-dom";
import { BrowserRouter, Route, Routes, Link } from "react-router-dom";
import { Button } from 'semantic-ui-react'
import SearchPage from './SearchPage.js';
import CreatePage from './CreatePage.js';
import PropertyOptions from './PropertyOptions.js';
import HomePage from './HomePage.js';

class App extends Component {
  constructor(props) {
    super(props);
  }
		
  render() {
	  return (
	  <div>
			<div>
				<BrowserRouter>
					<Link to="/">
						<Button style={{"width":"10vw","height": "7vh", "font-size": "2vh"}} type="button">
							<p>Home</p>
						</Button>
					</Link>
					<Link to="/create-property">
						<Button style={{"width":"10vw","height": "7vh", "font-size": "2vh"}} type="button">
							<p>Create Properties</p>
						</Button>
					</Link>
					<Link to="/search-properties">
						<Button style={{"width":"10vw","height": "7vh", "font-size": "2vh"}} type="button">
							<p>Search Properties</p>
						</Button>
					</Link>
					<Routes>
						<Route exact path="/" element={<HomePage />} />
						<Route path='/create-property' element={<CreatePage />} />
						<Route path='/search-properties' element={<SearchPage />} />
						<Route path='/update-property-:propertyId' element={<PropertyOptions />} />
						<Route path='/delete-property-:propertyId' element={<PropertyOptions />} />
					</Routes>
				</BrowserRouter>
			</div>
	  </div>
	  )
  }
}

export default App;

const container = document.getElementById("api");
render(<App />, container);
