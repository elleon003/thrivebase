/**
 * Dynamically loads an external script and returns a promise
 * @param {string} src - The source URL of the script to load
 * @returns {Promise} - Resolves when the script is loaded, rejects on error
 */
export function loadScript(src) {
  return new Promise((resolve, reject) => {
    // Check if script is already loaded
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = src
    script.async = true

    script.onload = () => resolve()
    script.onerror = () => reject(new Error(`Failed to load script: ${src}`))

    document.head.appendChild(script)
  })
}
