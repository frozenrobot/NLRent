import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Button } from 'semantic-ui-react';
import { CSVLink } from "react-csv";
 
class SearchForm extends Component {
	
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      csvData: [],
      csvHeaders: [
      { label: "externalId", key: "externalId" },
      { label: "city", key: "city" },
      { label: "latitude", key: "latitude" },
      { label: "longitude", key: "longitude" },
      { label: "rent", key: "rent" },
      { label: "areaSqm", key: "areaSqm" },
      { label: "isRoomActive", key: "isRoomActive" },
      { label: "deposit", key: "deposit" },
      { label: "costPerSqm", key: "costPerSqm" }
      ],
      isLoaded: false,
      value: '',
      optionalOne: '',
      optionalTwo: '',
      optionalOneValue: '',
      optionalTwoValue: '',
      propertyTypeValue: 'room-',
      orderValue: 'ascending'
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.exportToJson = this.exportToJson.bind(this);
    this.downloadCsv = this.downloadCsv.bind(this);
  }
  
  componentDidMount() {
	switch (this.props.optional) {
		case "budget": {
			this.setState({optionalOne: "&min="});
			this.setState({optionalTwo: "&max="});
			break;
		}
		case "top-n": {
			this.setState({optionalOne: "&order="});
			this.setState({optionalTwo: "&n="});
			break;
		}
		case "lat-long": {
			this.setState({optionalOne: "?lat="});
			this.setState({optionalTwo: "&long="});
			if (this.props.search==="other") {
				this.setState({
					csvHeaders: [
					  { label: "plusCode", key: "plusCode" },
					  { label: "principalSubdivision", key: "principalSubdivision" },
					  { label: "principalSubdivisionCode", key: "principalSubdivisionCode" },
					  { label: "locality", key: "locality" },
					  ]
				})
			}
			break;
		}
		case "": {
			if (this.props.search==="other") {
				this.setState({
					csvHeaders: [
					  { label: "meanRentalCost", key: "Mean Rental Cost" },
					  { label: "medianRentalCost", key: "Median Rental Cost" },
					  { label: "standardDeviationRentalCost", key: "Standard Deviation in Rental Cost" },
					  { label: "meanDeposit", key: "Mean Deposit" },
					  { label: "medianDeposit", key: "Median Deposit" },
					  { label: "standardDeviationDeposit", key: "Standard Deviation in Deposit" },
					  ]
				})
			}
			break;
		}
	}
  }

  handleChange(event) {
	this.setState({
		[event.target.name]: event.target.value
	});
  }
   
   fetchJsonRequest() {
	   var prefixValue = ''
	   var orderValue = ''
	   var optionalValue = this.state.optionalTwo;
	   if (this.props.link === "property/") {
		   prefixValue = this.state.propertyTypeValue
	   }
	   if (this.props.optional == "top-n") {
		   orderValue = this.state.orderValue;
		   if (this.state.optionalTwoValue==='') {
			   optionalValue = '';
		   }
	   }
	   let lookupOptions = {
		   method: "GET",
			headers: {
				'Content-Type': 'application/json',
			}
	   }
	  fetch("api/"+this.props.link+prefixValue+this.state.value+this.state.optionalOne+
	  this.state.optionalOneValue+orderValue+optionalValue+this.state.optionalTwoValue, lookupOptions)
	 .then(response => {
		 if (response.status==204) {
			 alert("Could not retrieve any properties for this search!");
		 } if (response.status==400) {
			alert("Required parameter is missing!");
		 } if (response.status==500) {
			alert("Server Error!");
		 } else {
			return response.json()
			 .then((result) => {
				 this.setState(() => {
					 return {
						 isLoaded: true,
						 data: result,
						 csvData: this.toArray(result)
					 }
				 });
			})
		 }
	  })
  }
  
  toArray(json) {
	  if (!Array.isArray(json)) {
		  return [json];
	  } else {
		  return json;
	  }
  }

  handleSubmit(event) {
	  event.preventDefault();
	  this.setState({
		  data: [],
		  csvData: []
	  });
	  this.fetchJsonRequest();
  }
  
  getCityPropertyPlaceholder() {
	  if (this.props.link === "property/") {
		  return "Property ID";
	  } else {
		  return "City";
	  }
  }
  
  downloadFile({data, fileName, fileType}) {
	  const blob = new Blob([data], { type: fileType });
	  const href = URL.createObjectURL(blob);
	  const link = document.createElement('a');
	  link.href = href;
	  link.download = fileName;
	  document.body.appendChild(link);
	  link.click();
	  document.body.removeChild(link);
  }
  
  exportToJson(event) {
	  event.preventDefault();
	  this.downloadFile({
		  data: JSON.stringify(this.state.data),
		  fileName: "MyData.json",
		  fileType: "text/json"
	  })
  }
  
  downloadCsv(event) {
	  event.preventDefault();
	  this.csvAnchor.link.click();
  }
  
  render() {
	  const csvReport = {
		  data: this.state.csvData, 
		  headers: this.state.csvHeaders, 
		  filename: "MyData.csv"};
	  return (
	  <div style={{"width":"100vw", "text-align":"center", "clear":"both"}}>
			  <span style={{"font-size": "3vh"}}>{this.props.info}</span>
			  {this.props.link === "property/" && <select style={{"height": "6vh", "font-size": "2vh"}} name="propertyTypeValue" defaultValue={this.state.propertyTypeValue} onChange={this.handleChange}>
					<optgroup label = "Property Type" />
					<option value="room-">room</option>
					<option value="studio-">studio</option>
					<option value="apartment-">apartment</option>
					<option value="anti-squat-">anti-squat</option>
					<option value="student%20residence-">student residence</option>
              </select>}
			  {this.props.optional !== "lat-long" && <input style={{"height": "5vh", "font-size": "2vh"}} type="text" name="value" value={this.state.value} placeholder={this.getCityPropertyPlaceholder()} onChange={this.handleChange} />}
			  {this.props.optional !== "" && this.props.optional !== "top-n" && <input style={{"height": "5vh", "font-size": "2vh"}} type="text" name="optionalOneValue" value={this.state.optionalOneValue} placeholder={this.state.optionalOne} onChange={this.handleChange} />}				
			  {this.props.optional === "top-n" && <select style={{"height": "6vh", "font-size": "2vh"}} name="orderValue" defaultValue={this.state.orderValue} onChange={this.handleChange}>
				  <option value="ascending">ascending</option>
				  <option value="descending">descending</option>
			  </select>}
			  {this.props.optional !== "" && <input style={{"height": "5vh", "font-size": "2vh"}} type="text" name="optionalTwoValue" value={this.state.optionalTwoValue} placeholder={this.state.optionalTwo} onChange={this.handleChange} />}
			<Button type="button" style={{"height": "7vh", "font-size": "2vh"}}  onClick={this.handleSubmit}>
				<p>Search</p>
		    </Button>
		    <Button type="button" style={{"height": "7vh", "font-size": "2vh"}} onClick={this.exportToJson}>
				<p>Download .json</p>
		    </Button>
				<CSVLink style={{ textDecoration: "none" }} ref={(reference) => this.csvAnchor = reference} {...csvReport} ></CSVLink>
		    <Button type="button" style={{"height": "7vh", "font-size": "2vh"}} onClick={this.downloadCsv}>
				<p>Download .csv</p>
		    </Button>
		  <br></br>
		  <details open><summary>Show/Hide Results</summary>
		  <div style={{"width": "60%", "padding-left":"20%", "padding-right":"20%", "margin-bottom": "1vh"}}>
			{this.props.search !== "other" && this.state.data.map((property, i) => (
				<div style={{"border": "1px solid black", "float": "left", "width": "32.33%"}} key={property.externalId}>
					{Object.entries(property).map(([key, value], index) => (
							<div style={{"width": "100%"}}>
								<span style={{"font-weight":"bold", "text-align":"left", "font-size":"1.5em"}} key={index}>{key}:</span>
								<span style={{"text-align":"center", "font-size":"1.5em"}} key={key}>{value}</span>
							</div>
					))}
					<Link to={"/update-property-"+property.externalId} state={{propertyToUpdate : property, mode: "update"}}>
						<Button style={{"height": "7vh", "font-size": "2vh"}} type="button">
							<p>Update Property</p>
						</Button>
					</Link>
					<br></br>
					<Link to={"/delete-property-"+property.externalId} state={{propertyToUpdate : property, mode: "delete"}}>
						<Button style={{"height": "7vh", "font-size": "2vh"}} type="button">
							<p>Delete Property</p>
						</Button>
					</Link>
					<br></br>
				</div>
			))}
		  </div>
		  <br></br>
		  <div style={{"width": "20%", "padding-left":"40%", "padding-right":"40%"}}>
		  {this.props.search === "other" &&
					Object.entries(this.state.data).map(([key, value], index) => {
						return (
							<div style={{"width": "100%", "border": "1px solid black"}}>
								<span style={{"font-weight":"bold", "font-size":"1.5em"}} key={index}>{key}:</span>
								<span style={{"text-align":"center", "font-size":"1.5em"}} key={key}>{value}</span>
							</div>
						);
					})
				}
		  </div>
		  </details>
		  <br></br>
		</div>
	  );
  }
}

export default SearchForm
