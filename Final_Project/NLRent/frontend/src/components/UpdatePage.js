import React, { Component } from 'react';
import { Button } from 'semantic-ui-react';
import { Link } from "react-router-dom";

class UpdatePage extends Component {
	
	constructor(props) {
		super(props);
		this.state = {
			error: null,
			externalId: this.props.propertyToUpdate.externalId,
			cityValue: this.props.propertyToUpdate.city,
			latitudeValue: this.props.propertyToUpdate.longitude,
			longitudeValue: this.props.propertyToUpdate.latitude,
			rentValue: this.props.propertyToUpdate.rent,
			areaValue: this.props.propertyToUpdate.areaSqm,
			roomActiveValue: this.props.propertyToUpdate.isRoomActive,
			depositValue: this.props.propertyToUpdate.deposit,
			postMethod: "PATCH"
		}
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}
	
	emptyValues() {
		if (this.state.cityValue==='' || this.state.latitudeValue==='' || this.state.rentValue==='' || 
		this.state.longitudeValue==='' || this.state.areaValue==='' || this.state.depositValue==='') {
			alert("You missed a field!");
			return true;
		} else {
			return false;
		}
	}
	
    handleChange(event) {
		this.setState({
			[event.target.name]: event.target.value
		});
	}
	
    handleSubmit(event) {
		if (this.emptyValues()) {
			event.preventDefault();
		} else {
			this.updateProperty();
		}
	}
	
	updateProperty(){
		let data = {"externalId": this.state.externalId,  "city": this.state.cityValue, 
			"latitude": this.state.latitudeValue, "longitude": this.state.longitudeValue,  "rent": parseFloat(this.state.rentValue), 
			"areaSqm": parseFloat(this.state.areaValue), "isRoomActive": this.state.roomActiveValue, "deposit": parseFloat(this.state.depositValue)};
		let lookupOptions = {
			method: this.state.postMethod,
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
			credentials: 'include'
		};
		const endpoint = 'api/property/'+this.state.externalId+"/";
		fetch(endpoint, lookupOptions)
		.then(function(response) {
			if (response.status<204) {
				alert("Property succesfully updated!")
			} else {
				alert("No property with such ID!");
			}
		})
	}
	
  render() {
    return (
		<div style={{"width":"40%", "padding-left": "30%", "padding-right": "30%"}}>
			<br></br>
			<div style={{"height": "6vh"}}>
				<span style={{"font-size": "3vh", "float":"left"}}>City: </span>
				<input style={{"height": "5vh", "font-size": "2vh", "float": "right"}} type="text" name="cityValue"  value={this.state.cityValue} placeholder="City" onChange={this.handleChange} />
			</div>
			<div style={{"height": "6vh"}}>
				<span style={{"font-size": "3vh", "float":"left"}}>Latitude: </span>
				<input style={{"height": "5vh", "font-size": "2vh", "float": "right"}} type="text" name="latitudeValue"  value={this.state.latitudeValue} placeholder="Latitude" onChange={this.handleChange} />
			</div>
			<div style={{"height": "6vh"}}>
				<span style={{"font-size": "3vh", "float":"left"}}>Longitude: </span>
				<input style={{"height": "5vh", "font-size": "2vh", "float": "right"}} type="text" name="longitudeValue"  value={this.state.longitudeValue} placeholder="Longitude" onChange={this.handleChange} />
			</div>		
			<div style={{"height": "6vh"}}>
				<span style={{"font-size": "3vh", "float":"left"}}>Rent: </span>
				<input style={{"height": "5vh", "font-size": "2vh", "float": "right"}} type="text" name="rentValue"  value={this.state.rentValue} placeholder="Rent" onChange={this.handleChange} />
			</div>		
			<div style={{"height": "6vh"}}>
				<span style={{"font-size": "3vh", "float":"left"}}>Area m²: </span>
				<input style={{"height": "5vh", "font-size": "2vh", "float": "right"}} type="text" name="areaValue"  value={this.state.areaValue} placeholder="Area m²" onChange={this.handleChange} />
			</div>			
			<div style={{"height": "6vh"}}>
				<span style={{"font-size": "3vh", "float":"right", "float":"left"}}>Currently Active? </span>
				<select style={{"height": "5vh", "font-size": "2vh", "float": "right"}} name="roomActiveValue" defaultValue={this.state.roomActiveValue} onChange={this.handleChange}>
					<optgroup label = "Currently Active?" />
					<option value="true">true</option>
					<option value="false">false</option>
				</select>
			</div>		
			<div style={{"height": "6vh"}}>
				<br></br>
				<span style={{"font-size": "3vh", "float":"left"}}>Deposit: </span>
				<input style={{"height": "5vh", "font-size": "2vh", "float": "right"}} type="text" name="depositValue"  value={this.state.deposit} value={this.state.depositValue} placeholder="Deposit" onChange={this.handleChange} />
			</div>		
			<br></br>
			<div style={{"height": "6vh"}}>
				<Link to={"/"}>
					<Button style={{"height": "7vh", "font-size": "2vh"}} type="button" onClick={this.handleSubmit}>
						<p>Update Property</p>
					</Button>
				</Link>
			</div>		
			<br></br>
			<br></br>
		</div>
    );
  }
}

export default UpdatePage;
