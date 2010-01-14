/*
File:   jquery.socialauth.js
This file is used to define some javascript functionality to enable seamless
integration of the various social authentication mechanisms into the site.

Section:    Version History
08/09/2009 (DJO) - Created File
*/

// define the social auth namespace and global utility classes and functions
jQuery.socialAuth = {
    detailsDisplayed: false
}; // jQuery.socialAuth

// socialAuthLogin jQuery plugin
jQuery.fn.socialAuthLogin = function(opts) {

}; // fn.socialAuthLogin


jQuery(document).ready(function() {
    // alert("social auth included");
    $("a.signin").click(function() {
        // toggle the details displayed flag
        jQuery.socialAuth.detailsDisplayed = !jQuery.socialAuth.detailsDisplayed;
    
        // show or hide the login details area depending on the 
        if (jQuery.socialAuth.detailsDisplayed) {
            $("#logindetails").show();
        }
        else {
            $("#logindetails").hide();
        } // if..else
    }); // click
});
