import React from 'react';
import { useLocation } from "react-router-dom";
import UpdatePage from './UpdatePage.js';
import DeletePage from './DeletePage.js';

function PropertyOptions () {
	const location = useLocation()
	const { propertyToUpdate } = location.state;
	const { mode } = location.state;
	
	return (
	  <div>
		{mode==="update" && <UpdatePage propertyToUpdate={propertyToUpdate} />}
		{mode==="delete" &&  <DeletePage propertyToUpdate={propertyToUpdate} />}
	  </div>
	)
}

export default PropertyOptions;
