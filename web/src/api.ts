// import React, { useState, useEffect } from 'react';

const API_ENDPOINT = "http://127.0.0.1:8000/"

export const fetchRoot = async () => {
try {
const response = await fetch(API_ENDPOINT);
const json = await response.json();
console.log(json)
} catch (error) {
console.error(error);
}
};