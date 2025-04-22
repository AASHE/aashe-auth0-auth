# AASHE Auth0 Snippets

Contains versioned snippets of code used in the Auth0 management dashboard.

## Tricke user migration

Login function (Authentication/Database/Custom Database):

```
function login(email, password, callback) {
  
  function getMembersuiteIndividualAndReturn(token, user, callback) {
    const https = require('https');
    const options = {
      hostname: 'rest.membersuite.com',
      port: 443,
      path: '/crm/v1/individuals/25979?ID=' + user.ownerId,
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + token,
      }
    };

    // Create a request object
    const request = https.request(options, (response) => {
      // Initialize a variable to store the response data
      let data = '';

      // Listen to the data event
      response.on('data', (chunk) => {
        // Append the chunk to the data variable
        data += chunk.toString();
      });

      // Listen to the end event
      response.on('end', () => {
        // Parse the data as JSON
        const ms_individual = JSON.parse(data);
        
        callback(null, {
          user_id: "ms" + user.userId.slice(8),
          nickname: user.firstName + " " + user.lastName,
          email: user.email,
          first_name: user.firstName,
          last_name: user.lastName,
          app_metadata: {
            "origin": "membersuite_lazy",
          	"receives_member_benefits": user.receivesMemberBenefits,
            "ms_owner_id": user.ownerId,
            "ms_organization_id": ms_individual.primaryOrganization__rtg
          }
        });
      });

      // Listen to the error event
      response.on('error', (error) => {
        // Throw the error
        throw error;
      });
    });

    // End the request object
    request.end();
  }

  function getUserData(token, callback){
    const https = require('https');
    const options = {
      hostname: 'rest.membersuite.com',
      port: 443,
      path: '/platform/v2/whoami',
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + token,
      }
    };

    // Create a request object
    const request = https.request(options, (response) => {
      // Initialize a variable to store the response data
      let data = '';

      // Listen to the data event
      response.on('data', (chunk) => {
        // Append the chunk to the data variable
        data += chunk.toString();
      });

      // Listen to the end event
      response.on('end', () => {
        // Parse the data as JSON
        const user = JSON.parse(data);

        getMembersuiteIndividualAndReturn(token, user, callback);
      });

      // Listen to the error event
      response.on('error', (error) => {
        // Throw the error
        throw error;
      });
    });

    // End the request object
    request.end();
  }
  
  // Import the http module
  const https = require('https');
  // Create an options object
  const options = {
    hostname: 'rest.membersuite.com',
    port: 443,
    path: '/platform/v2/loginUser/25979',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'Node.js'
    }
  };

  // Create a data object
  const data = {
    email: email,
    password: password,
  };

  // Stringify the data object
  const dataString = JSON.stringify(data);

  // Update the options object with the data length
  options.headers['Content-Length'] = dataString.length;

  // Create a request object
  const request = https.request(options, (response) => {
    // Initialize a variable to store the response data
    let data = '';

    // Listen to the data event
    response.on('data', (chunk) => {
      // Append the chunk to the data variable
      data += chunk.toString();
    });

    // Listen to the end event
    response.on('end', () => {
      if (response.statusCode === 401) {
      	return callback(new Error(data));
      }
      // Parse the data as JSON
      const resp = JSON.parse(data);
      
      if(resp.success) {
        getUserData(resp.data.accessToken, callback);
      } else {
        return callback(new Error(resp.firstErrorMessage));
      }
    });

    // Listen to the error event
    response.on('error', (error) => {
      // Throw the error
      throw error;
    });
  });
  // Write the data to the request object
  request.write(dataString);
  // End the request object
  request.end();
}


```
