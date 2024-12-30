const axios = require('axios');

const candidateId = '7cbdcb04-f31f-4fce-98dd-fa9b2b0d67e5';
const baseURL = 'https://challenge.crossmint.io/api/polyanets';

// Function to create Polyanet at a specific row and column with retries
async function createPolyanet(row, column, retries = 3) {
    try {
        const response = await axios.post(`${baseURL}`, {
            row: row,
            column: column,
            candidateId: candidateId
        });
        console.log(`Polyanet created at [${row}, ${column}]`);
    } catch (error) {
        console.error(`Failed to create Polyanet at [${row}, ${column}]`);
        if (retries > 0) {
            console.log(`Retrying for [${row}, ${column}]...`);
            await createPolyanet(row, column, retries - 1);
        }
    }
}

// Function to create an X-shape in an 11x11 grid
async function createXShape() {
    const positions = [
         [8,8]
    ];

    for (let pos of positions) {
        await createPolyanet(pos[0], pos[1]);
    }
}

// Start creating the X-shape
createXShape();


// // Function to delete a Polyanet at a specific row and column
// async function deletePolyanet(row, column) {
//     try {
//         const response = await axios.delete(`${baseURL}`, {
//             data: {
//                 row: row,
//                 column: column,
//                 candidateId: candidateId
//             }
//         });
//         console.log(`Polyanet deleted at [${row}, ${column}]`);
//     } catch (error) {
//         console.error(`Failed to delete Polyanet at [${row}, ${column}]`);
//     }
// }

// // Function to reset all positions in the X-shape to empty space
// async function resetMatrix() {
//     const positions = [
//         [1,9]
//     ];

//     for (let pos of positions) {
//         await deletePolyanet(pos[0], pos[1]);
//     }
// }

// // Start resetting the matrix
// resetMatrix();
