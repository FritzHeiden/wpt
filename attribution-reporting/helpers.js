/**
 * Helper functions for attribution reporting API tests.
 */

/**
 * Method to clear the stash. Takes the URL as parameter. This could be for
 * event-level or aggregatable reports.
 */
const clearStash = (url) => {
  const options = {
    method: "POST",
    body: JSON.stringify({ clear_stash: true }),
  };
  return fetch(url, options)
}

/**
 * Registers either a source or trigger.
 */
const register = (url) => {
  const image = document.createElement("img");
  image.setAttribute("attributionsrc", url);
}

/**
 * Delay method that waits for prescribed number of miliseconds.
 */
const delay = ms => new Promise(resolve => step_timeout(resolve, ms));

/**
 * Method that polls a particular URL every interval for reports. Once reports are
 * received, returns the payload as promise.
 */
const poll = async (url, interval) => {
  const resp = await fetch(url);
  const payload = await resp.json();
  if (payload.reports.length === 0) {
    await delay(interval);
    return poll(url);
  }
  return new Promise(resolve => resolve(payload));
}
