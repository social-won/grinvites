// import React, { useState, useEffect } from 'react';

const API_ENDPOINT = "http://127.0.0.1:8000"

export const fetchRoot = async () => {
    try {
        const response = await fetch(API_ENDPOINT);
        const json = await response.json();
        console.log(json)
    } catch (error) {
        console.error(error);
    }
};

export const fetchMe = async () => {
    try {
        const response = await fetch(`${API_ENDPOINT}/user/1`, {
            credentials: "include",
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            if (response.status === 401) {
                return null;
            }
            throw new Error(`Failed to fetch user: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error fetching user:", error);
        throw error;
    }
};


export const classesData = [
    { id: "ART-101-01", name: "ART-101-01" },
    { id: "ANT-104-01", name: "ANT-104-01" },
    { id: "CSC-161-01", name: "CSC-161-01" },
    { id: "ECN-220-02", name: "ECN-220-02" },
    { id: "SPN-101-01", name: "SPN-101-01" },
    { id: "SOC-334-01", name: "SOC-334-01" }
  ];

export const hoursData = [
    { id: "bear", name: "Bear" },
    { id: "fitness-center", name: "Fitness center" },
    { id: "pool", name: "Pool" },
    { id: "spencer-grill", name: "Spencer Grill" },
    { id: "dining-hall", name: "Dining Hall" },
    { id: "academic-building", name: "Academic Building" },
    { id: "golf-course", name: "Golf Course" }
  ];

export const interestsData = [
    { id: "bear", name: "Bear" },

]