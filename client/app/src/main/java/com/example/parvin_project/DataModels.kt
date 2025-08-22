// DataModels.kt
package com.example.porteghal
import com.google.gson.annotations.SerializedName
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
    @SerializedName("plmn_id")
    val plmnId: String? = null,
    val lac: Int? = null,
    val tac: Int? = null,
    val rac: Int? = null, // Not available via public APIs
    @SerializedName("cell_id")
    val cellId: Long? = null,

    // Frequency Parameters
    @SerializedName("frequency_band")
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
    @SerializedName("error_message")
    val errorMessage: String? = null
)


data class Signal(
    val timestamp: String?, // ISO 8601 format (e.g., "2024-06-14T12:00:00Z")

    val technology: String? = null,
    val plmn_id: String? = null,
    val lac: Int? = null,
    val tac: Int? = null,
    val rac: Int? = null,
    val cell_id: Long? = null,

    // Frequency Parameters
    val frequency_band: String? = null,
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
    val dns_response_time: Double?, // ms
    val ping_response_time: Double?, // ms
    val sms_delivery_time: Double?, // ms (was Int in OpenAPI, but your code generates Double for durationMs)

    val longitude: Double?,
    val latitude: Double?,
)

data class RequestBody(
    val measurements: List<Signal>
)