import React, { Component } from "react";
import { render } from "react-dom";
import SearchForm from './SearchForm.js';

class SearchPage extends Component {
  constructor(props) {
    super(props);
  }
		
  render() {
	  return (
	  //Note that search="property" gets an array of objects and search="other" gets just a single object
		<div>
			<br></br>
			<div>
				<SearchForm search="property" optional="lat-long" link="properties/" info="Search properties by latitude and longitude:" />
			</div>
			<div>
				<SearchForm search="other" optional="lat-long" link="properties/extra/" info="Extra information based on latitude and longitude:" />
			</div>
			<div>
				<SearchForm search="property" optional="budget" link="properties/budget/?city=" info="Search properties by city and budget:" />
			</div>
			<div>
				<SearchForm search="property" optional="" link="properties/city/?city=" info="Search properties by city:" />
			</div>
			<div>
				<SearchForm search="property" optional="" link="property/" info="Search properties by ID:" />
			</div>
			<div>
				<SearchForm search="other" optional="" link="statistics/?city=" info="Search city for statistics:" />
			</div>
			<div>
				<SearchForm search="Nproperty" optional="top-n" link="properties/top-rent/?city=" info="Search the top N properties in a city by rent:" />
			</div>
			<div>
				<SearchForm search="Nproperty" optional="top-n" link="properties/top-cost-per-sqm/?city=" info="Search the top N properties in a city by cost per square meter:" />
			</div>
		</div>
		)
  }
}

export default SearchPage;
