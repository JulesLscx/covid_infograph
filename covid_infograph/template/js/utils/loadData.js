export function loadData(url) {
  return new Promise((resolve, reject) => {
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        // Vérifier si les données sont valides
        if (!Array.isArray(data)) {
          throw new Error("Invalid data format: expected an array.");
        }
        // Renvoyer les données sous forme de tableau
        resolve(data);
      })
      .catch((error) => {
        console.error(`Error fetching data: ${error}`);
        reject(error);
      });
  });
}
