// DataModels.kt
package com.example.parvin_project

/**
 * Data class to hold collected Location information.
 * @param latitude The latitude.
 * @param longitude The longitude.
 * @param status A string indicating the status of location fix (e.g., "Fixed", "Waiting for fix", "Providers disabled").
 */
data class LocationData(
    val latitude: Double?,
    val longitude: Double?,
    val status: String
)

data class CellInfoData(
    // Identity Parameters
    val technology: String? = null,
    val plmnId: String? = null,
    val lac: Int? = null,
    val tac: Int? = null,
    val rac: Int? = null, // Not available via public APIs
    val cellId: Long? = null,

    // Frequency Parameters
    val frequencyBand: String? = null,
    val arfcn: Int? = null,
    val earfcn: Int? = null,
    val uarfcn: Int? = null,
    val nrarfcn: Int? = null,
    val frequencyHz: Long? = null,

    // Signal Quality Parameters
    val rsrp: Int? = null,
    val rsrq: Int? = null,
    val rscp: Int? = null,
    val ecNo: Int? = null,
    val rxLev: Int? = null,

    // Status Message
    val errorMessage: String? = null
)


data class Signal(
    val record_time: String?, // ISO 8601 format (e.g., "2024-06-14T12:00:00Z")

    val technology: String? = null,
    val plmnId: String? = null,
    val lac: Int? = null,
    val tac: Int? = null,
    val rac: Int? = null, // Not available via public APIs
    val cellId: Long? = null,

    // Frequency Parameters
    val frequencyBand: String? = null,
    val arfcn: Int? = null,
    val earfcn: Int? = null,
    val uarfcn: Int? = null,
    val nrarfcn: Int? = null,
    val frequencyHz: Long? = null,

    // Signal Quality Parameters
    val rsrp: Int? = null,
    val rsrq: Int? = null,
    val rscp: Int? = null,
    val ecNo: Int? = null,
    val rxLev: Int? = null,

    val download_rate: Double?, // KB/s
    val upload_rate: Double?, // KB/s
    val dns_lookup_rate: Double?, // ms
    val ping: Double?, // ms
    val sms_delivery_time: Double?, // ms (was Int in OpenAPI, but your code generates Double for durationMs)

    val longitude: Double?,
    val latitude: Double?,
)

data class RequestBody(
    val signals: List<Signal>
)