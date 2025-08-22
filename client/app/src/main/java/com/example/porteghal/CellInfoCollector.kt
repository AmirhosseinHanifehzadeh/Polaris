package com.example.porteghal

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.telephony.*
import android.util.Log
import androidx.core.content.ContextCompat

class CellInfoCollector(private val context: Context) {
    private val telephonyManager: TelephonyManager =
        context.getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager

    fun getCellInfoData(): CellInfoData {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return CellInfoData(errorMessage = "Location permission not granted. Cell information requires it.")
        }

        try {
            val cellInfoList: List<CellInfo>? = telephonyManager.allCellInfo

            if (cellInfoList.isNullOrEmpty()) {
                return CellInfoData(errorMessage = "No cell information available.")
            }

            for (cellInfo in cellInfoList) {
                if (cellInfo.isRegistered) {
                    return parseServingCellInfo(cellInfo)
                }
            }

            return CellInfoData(errorMessage = "No registered serving cell found.")
        } catch (e: SecurityException) {
            Log.e("CellInfoCollector", "Security Exception: ${e.message}")
            return CellInfoData(errorMessage = "Security Exception: Permission may be missing or revoked.")
        } catch (e: Exception) {
            Log.e("CellInfoCollector", "Error getting cell info: ${e.message}", e)
            return CellInfoData(errorMessage = "An unexpected error occurred while fetching cell info.")
        }
    }

    private fun parseServingCellInfo(cellInfo: CellInfo): CellInfoData {
        return when (cellInfo) {
            is CellInfoGsm -> parseGsm(cellInfo)
            is CellInfoWcdma -> parseWcdma(cellInfo)
            is CellInfoLte -> parseLte(cellInfo)
            else -> CellInfoData(technology = "Unknown", errorMessage = "Unsupported cell type: ${cellInfo::class.java.simpleName}")
        }
    }

    private fun parseGsm(cellInfo: CellInfoGsm): CellInfoData {
        val identity = cellInfo.cellIdentity
        val signal = cellInfo.cellSignalStrength
        val arfcn = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) identity.arfcn else null

        // Ensure 'band' is a non-nullable String by providing a default value if arfcn is null
        val band: String = if (arfcn != null) {
            getGsmBand(arfcn) // getGsmBand (from your helpers) returns non-nullable String
        } else {
            "Unknown GSM" // Provide a default non-nullable string for the band
        }

        return CellInfoData(
            technology = "GSM",
            plmnId = getPlmnId(identity.mccString, identity.mncString),
            lac = identity.lac.takeIf { it != CellInfo.UNAVAILABLE },
            cellId = identity.cid.toLong().takeIf { it != CellInfo.UNAVAILABLE.toLong() },
            arfcn = arfcn?.takeIf { it != CellInfo.UNAVAILABLE },
            frequencyBand = band,
            frequencyHz = arfcn?.let { getGsmDownlinkFrequency(it, band) },
            rxLev = signal.dbm.takeIf { it != CellInfo.UNAVAILABLE }
        )
    }

    private fun parseWcdma(cellInfo: CellInfoWcdma): CellInfoData {
        val identity = cellInfo.cellIdentity
        val signal = cellInfo.cellSignalStrength
        val uarfcn = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) identity.uarfcn else null
        val band = uarfcn?.let { getUtranBand(it) }

        return CellInfoData(
            technology = "UMTS (WCDMA/HSPA)",
            plmnId = getPlmnId(identity.mccString, identity.mncString),
            lac = identity.lac.takeIf { it != CellInfo.UNAVAILABLE },
            cellId = identity.cid.toLong().takeIf { it != CellInfo.UNAVAILABLE.toLong() },
            uarfcn = uarfcn?.takeIf { it != CellInfo.UNAVAILABLE },
            frequencyBand = band,
            frequencyHz = uarfcn?.let { getUtranDownlinkFrequency(it) },
            rscp = signal.dbm.takeIf { it != CellInfo.UNAVAILABLE },
        )
    }

    private fun parseLte(cellInfo: CellInfoLte): CellInfoData {
        val identity = cellInfo.cellIdentity
        val signal = cellInfo.cellSignalStrength
        val earfcn = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) identity.earfcn else null
        val bands = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) identity.bands else intArrayOf()
        val bandName = getLteBand(earfcn, bands)

        return CellInfoData(
            technology = "LTE",
            plmnId = getPlmnId(identity.mccString, identity.mncString),
            tac = identity.tac.takeIf { it != CellInfo.UNAVAILABLE },
            cellId = identity.ci.toLong().takeIf { it != CellInfo.UNAVAILABLE.toLong() },
            earfcn = earfcn?.takeIf { it != CellInfo.UNAVAILABLE },
            frequencyBand = bandName,
            frequencyHz = earfcn?.let { getLteDownlinkFrequency(it) },
            rsrp = signal.rsrp.takeIf { it != CellInfo.UNAVAILABLE },
            rsrq = signal.rsrq.takeIf { it != CellInfo.UNAVAILABLE }
        )
    }

    // --- Helper Functions ---

    private fun getPlmnId(mcc: String?, mnc: String?): String? {
        if (mcc.isNullOrEmpty() || mnc.isNullOrEmpty()) return null
        return "$mcc-$mnc"
    }

}
