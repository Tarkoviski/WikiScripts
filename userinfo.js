// Adapted from http://en.wikipedia.org/wiki/w:User:PleaseStand/User_info

function UserinfoJsFormatQty(qty, singular, plural) {
	return String(qty).replace(/\d{1,3}(?=(\d{3})+(?!\d))/g, "$&,") + "\u00a0" + (qty == 1 ? singular : plural);
}

function UserinfoJsFormatDateRel(old) {
	// The code below requires the computer's clock to be set correctly.
	var age = new Date().getTime() - old.getTime();
	var ageNumber, ageRemainder, ageWords;
	if (age < 60000) {
		// less than one minute old
		ageNumber = Math.floor(age / 1000);
		ageWords = UserinfoJsFormatQty(ageNumber, "second", "seconds");
	} else if (age < 3600000) {
		// less than one hour old
		ageNumber = Math.floor(age / 60000);
		ageWords = UserinfoJsFormatQty(ageNumber, "minute", "minutes");
	} else if (age < 86400000) {
		// less than one day old
		ageNumber = Math.floor(age / 3600000);
		ageWords = UserinfoJsFormatQty(ageNumber, "hour", "hours");
		ageRemainder = Math.floor((age - ageNumber * 3600000) / 60000);
	} else if (age < 604800000) {
		// less than one week old
		ageNumber = Math.floor(age / 86400000);
		ageWords = UserinfoJsFormatQty(ageNumber, "day", "days");
	} else if (age < 2592000000) {
		// less than one month old
		ageNumber = Math.floor(age / 604800000);
		ageWords = UserinfoJsFormatQty(ageNumber, "week", "weeks");
	} else if (age < 31536000000) {
		// less than one year old
		ageNumber = Math.floor(age / 2592000000);
		ageWords = UserinfoJsFormatQty(ageNumber, "month", "months");
	} else {
		// one year or older
		ageNumber = Math.floor(age / 31536000000);
		ageWords = UserinfoJsFormatQty(ageNumber, "year", "years");
		ageRemainder =
            Math.floor((age - ageNumber * 31536000000) / 2592000000);
		if (ageRemainder) {
			ageWords += " " +
                UserinfoJsFormatQty(ageRemainder, "month", "months");
		}
	}
	return ageWords;
}

// If on a user or user talk page, and not a subpage...
if ((mw.config.get("wgNamespaceNumber") == 2 || mw.config.get("wgNamespaceNumber") == 3) && !(/\//.test(mw.config.get("wgTitle")))) {
	// add a hook to...
	mw.loader.using(["mediawiki.util"], function () {
		$(function () {
			// Request the user's information from the API.
			// Note that this is allowed to be up to 5 minutes old.
			var et = encodeURIComponent(mw.config.get("wgTitle"));

			$.getJSON(mw.config.get("wgScriptPath") + "/api.php?format=json&action=query&list=users|usercontribs&usprop=blockinfo|editcount|gender|registration|groups&uclimit=1&ucprop=timestamp&ususers=" + et + "&ucuser=" + et + "&meta=allmessages&amprefix=grouppage-&amincludelocal=1")
				.done(function (query) {
					// When response arrives extract the information we need.
					if (!query.query) {
						return;
					} // Suggested by Gary King to avoid JS errors --PS 2010-08-25

					query = query.query;

					var user, invalid, missing, groups, editcount, registration, blocked, lastEdited;

					try {
						user = query.users[0];
						invalid = typeof user.invalid != "undefined";
						missing = typeof user.missing != "undefined";
						groups = (typeof user.groups == "object") ? user.groups : [];
						editcount = (typeof user.editcount == "number") ? user.editcount : null;
						registration = (typeof user.registration == "string") ?
							new Date(user.registration) : null;
						blocked = typeof user.blockedby != "undefined";
						lastEdited = (typeof query.usercontribs[0] == "object") &&
                            (typeof query.usercontribs[0].timestamp == "string") ?
							new Date(query.usercontribs[0].timestamp) : null;
					} catch (e) {
						return; // Not much to do if the server is returning an error (e.g. if the username is malformed).
					}

					// Format the information for on-screen display
					var statusText = "";

					if (blocked) {
						statusText += "<a href=\"" + mw.config.get("wgScriptPath") +
                            "/index.php?title=Special:Log&amp;page=" +
                            encodeURIComponent(mw.config.get("wgFormattedNamespaces")[2] + ":" + user.name) +
                            "&amp;type=block\">blocked</a> ";
					}

					if (missing) {
						statusText += "username not registered";
					} else if (invalid) {
						statusText += "invalid username";
					} else {
						var friendlyGroupNames = {
							"*": false,
							"user": false,
							"autoconfirmed": false,
							sysop: "administrator",
							suppress: "suppressor"
						};

						var friendlyGroups = [];

						for (var i = 0; i < groups.length; ++i) {
							var s = groups[i];
							var t = friendlyGroupNames.hasOwnProperty(s) ? friendlyGroupNames[s] : s;

							if (t) {
								friendlyGroups.push(t);
							}
						}

						switch (friendlyGroups.length) {
						case 0:
							if (blocked) {
								statusText += "user";
							} else {
								statusText += "registered user";
							}
							break;
						case 1:
							statusText += friendlyGroups[0];
							break;
						case 2:
							statusText += friendlyGroups[0] + " and " + friendlyGroups[1];
							break;
						default:
							statusText += friendlyGroups.slice(0, -1).join(", ") +
                                    ", and " + friendlyGroups[friendlyGroups.length - 1];
							break;
						}
					}

					// Registration date
					if (registration) {
						var firstLoggedUser = new Date("22:16, 7 September 2005"); // When the [[Special:Log/newusers]] was first activated
						if (registration >= firstLoggedUser) {
							statusText += ", <a href='" + mw.config.get("wgScriptPath") +
                                "/index.php?title=Special:Log&amp;type=newusers&amp;dir=prev&amp;limit=1&amp;user=" +
                                et + "'>" + UserinfoJsFormatDateRel(registration) + "</a> old";
						} else {
							statusText += ", <a href='" + mw.config.get("wgScriptPath") +
                                "/index.php?title=Special:ListUsers&amp;limit=1&amp;username=" +
                                et + "'>" + UserinfoJsFormatDateRel(registration) + "</a> old";
						}
					}

					// Edit count
					if (editcount !== null) {
						statusText += ", with " + UserinfoJsFormatQty(editcount, "edit", "edits");
					}

					// Prefix status text with correct article
					if ("AEIOaeio".indexOf(statusText.charAt(statusText.indexOf(">") + 1)) >= 0) {
						statusText = "An " + statusText;
					} else {
						statusText = "A " + statusText;
					}

					if (lastEdited) {
						statusText += ". Last edited <a href=\"" + mw.config.get("wgArticlePath").replace("$1", "Special:Contributions/" + encodeURIComponent(user.name)) + "\">" + UserinfoJsFormatDateRel(lastEdited) + " ago</a>.";
					}

					var ss = document.getElementById("siteSub");

					ss.innerHTML = "<span>" + statusText + "</span>";
					ss.style.display = "block";
				});
		});
	});
}
