import React, { Component } from 'react';
import { Button } from 'semantic-ui-react';
import { Link } from "react-router-dom";

class UpdatePage extends Component {
	
	constructor(props) {
		super(props);
		{/* Most likely issue is that it succesfuly has this.props.propertyToUpdate initialized but as soon as you refresh the state is gone and when it tries to access it, it's an indeterminate state. */}
		const splitIdArray = this.props.propertyToUpdate.externalId.split('-');
		this.state = {
			propertyTypeValue: splitIdArray[0]+'-',
			idValue: splitIdArray[1],
			postMethod: "DELETE"
		}
		this.handleSubmit = this.handleSubmit.bind(this);
	}
	
    handleSubmit(event) {
		this.deleteProperty();
	}
	
	deleteProperty(){
		let lookupOptions = {
			method: this.state.postMethod,
			headers: {
				'Content-Type': 'application/json',
			},
			credentials: 'include'
		};
		const endpoint = 'api/property/'+this.state.propertyTypeValue+this.state.idValue+"/";
		fetch(endpoint, lookupOptions)
		.then(function(response) {
			if (response.status<204) {
				alert("Property succesfully deleted!")
			} else {
				alert("No property with such ID!");
			}
		})
	}
	
  render() {
    return (
		<div>
			<br></br>
			<h1>Are you sure you want to permanently delete {this.state.propertyTypeValue+this.state.idValue}?</h1>
			<br></br><br></br>
			<Link to={"/"}>
				<Button style={{"height": "7vh", "font-size": "2vh"}} type="button" onClick={this.handleSubmit}>
					<p>Confirm Delete</p>
				</Button>
			</Link>
		</div>
    );
  }
}

export default UpdatePage;
