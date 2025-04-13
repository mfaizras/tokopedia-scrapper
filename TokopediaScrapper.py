import requests
import csv
import time
import random

class TokopediaScrapper:
    def __init__(self,keyword,csvFile="tokopedia_products.csv",type = 'a'):
        self.keyword = keyword
        self.csvFile = csvFile
        self.type = type
        self.userAgentList = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "ozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0",
            "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36 Edg/122.0.2365.92",
        ]
    
    def parse_price(self,price_str):
        # Hapus "Rp", titik, spasi, dan strip
        clean_str = (
            price_str.replace("Rp", "")
            .replace(".", "")
            .replace(",", "")
            .replace(" ", "")
            .replace("-", "")
        )
        try:
            return int(clean_str)
        except ValueError:
            return 0
    def get_product_page(self,url):
        print(f"   [{time.strftime('%Y-%m_%d-%H-%M-%S', time.gmtime())}] 📜 Get product Page {url}")
        headerProductPage = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(self.userAgentList),
        "Accept": "*/*",
        'Origin': 'https://www.tokopedia.com',
        'Referer': 'https://www.tokopedia.com/',
        'X-Tkpd-Akamai' : 'pdpGetLayout'
        }

        from urllib.parse import urlparse
        # Pisahkan path dari URL
        parsed = urlparse(url)
        parts = parsed.path.strip("/").split("/")

        urlQuery = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"

        # Extract slug toko dan slug produk
        shop_slug = parts[0]
        product_slug = parts[1]

        payload =   {
        "operationName": "PDPGetLayoutQuery",
        "variables": {
            "shopDomain": shop_slug,
            "productKey": product_slug,
            "layoutID": "",
            "apiVersion": 1,
            "tokonow": {
            "shopID": "",
            "whID": "",
            "serviceType": ""
            },
            "deviceID": "YjUxNmUwODM2YjNhZjZkMWNjMzNhNmNiMGVlN2YxY2NkYmZkZGU5NTZjMWU2YTFlMmUwZThhZDFhNzYxOWVkMDBmNzRhNDI5Zjk0YTRmYWNiZmM0ZTM5OGEyYjUxMGRm47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=",
            "userLocation": {
            "cityID": "176",
            "addressID": "",
            "districtID": "2274",
            "postalCode": "",
            "latlon": ""
            },
            "extParam": ""
        },
        "query": """    
        query PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $deviceID: String) {
        pdpGetLayout(
            shopDomain: $shopDomain
            productKey: $productKey
            layoutID: $layoutID
            apiVersion: $apiVersion
            userLocation: $userLocation
            extParam: $extParam
            deviceID: $deviceID
        ) {
            requestID
            name
            pdpSession
            basicInfo {
            alias
            createdAt
            productID
            shopID
            shopName
            defaultMediaURL
            minOrder
            maxOrder
            weight
            weightUnit
            condition
            status
            url
            sku
            gtin
            isMustInsurance
            needPrescription
            catalogID
            isBlacklisted
            isQA
            totalStockFmt
            sharingURL
            weightWording
            ttsPID
            ttsSKUID
            ttsShopID
            postATCLayout {
                layoutID
                __typename
            }
            menu {
                id
                name
                url
                __typename
            }
            category {
                id
                name
                title
                breadcrumbURL
                isAdult
                isKyc
                minAge
                detail {
                id
                name
                breadcrumbURL
                isAdult
                __typename
                }
                ttsID
                ttsDetail {
                id
                name
                breadcrumbURL
                isAdult
                __typename
                }
                __typename
            }
            blacklistMessage {
                title
                description
                button
                url
                __typename
            }
            txStats {
                transactionSuccess
                transactionReject
                countSold
                paymentVerified
                itemSoldFmt
                __typename
            }
            stats {
                countView
                countReview
                countTalk
                rating
                __typename
            }
            shopMultilocation {
                isReroute
                cityName
                eduLink {
                webLink {
                    action
                    query
                    __typename
                }
                __typename
                }
                __typename
            }
            __typename
            }
            additionalData {
            fomoSocialProofs {
                name
                icons
                text
                position
                backgroundColor
                typeIcon
                __typename
            }
            __typename
            }
            components {
            name
            type
            data {
                ...PdpDataProductMedia
                ...PdpDataProductContent
                ...PdpDataProductInfo
                ...PdpDataSocialProof
                ...PdpDataInfo
                ...PdpDataUpcomingCampaign
                ...PdpDataCustomInfo
                ...PdpDataProductDetail
                ...PdpDataProductVariant
                ...PdpDataOneLiner
                ...PdpDataDynamicOneLiner
                ...PdpDataCategoryCarousel
                ...pdpDataCustomInfoTitle
                ...PdpDataOnGoingCampaign
                ...PdpDataProductDetailMediaComponent
                ...PdpDataComponentSocialProofV2
                ...PdpDataComponentSDUIDivKit
                ...PdpDataProductListComponent
                ...PdpDataComponentPromoPrice
                ...PdpDataOneLinerVariant
                ...PdpDataComponentShipmentV4
                ...PdpDataComponentShipmentV5
                ...PdpDataComponentAffordabilityGroupLabel
                __typename
            }
            __typename
            }
            __typename
        }
        }
        
        fragment PdpDataProductVariant on pdpDataProductVariant {
        errorCode
        parentID
        defaultChild
        maxFinalPrice
        sizeChart
        componentType
        landingSubText
        postATCLayout {
            layoutID
            __typename
        }
        variants {
            productVariantID
            variantID
            name
            identifier
            option {
            picture {
                url
                url100
                __typename
            }
            productVariantOptionID
            variantUnitValueID
            value
            hex
            __typename
            }
            __typename
        }
        children {
            productID
            optionName
            isTopSold
            price
            priceFmt
            valuePriceFmt
            currencyFmt
            slashPriceFmt
            discPercentage
            sku
            optionID
            subText
            productName
            productURL
            sharingURL
            componentPriceType
            ttsPID
            ttsSKUID
            promo {
            ...PDPDataPromo
            __typename
            }
            labelIcons {
            ...PDPContentLabelIcon
            __typename
            }
            picture {
            url
            url100
            __typename
            }
            stock {
            stock
            isBuyable
            stockWording
            stockWordingHTML
            minimumOrder
            maximumOrder
            stockFmt
            stockCopy
            __typename
            }
            isCOD
            isWishlist
            campaignInfo {
            campaignID
            campaignType
            campaignTypeName
            campaignLogo
            discountPercentage
            originalPrice
            discountPrice
            stock
            stockSoldPercentage
            threshold
            startDate
            endDate
            endDateUnix
            appLinks
            isAppsOnly
            isActive
            hideGimmick
            showStockBar
            minOrder
            campaignIdentifier
            applink
            background
            paymentInfoWording
            __typename
            }
            thematicCampaign {
            ...PDPThematicCampaign
            __typename
            }
            ttsPID
            ttsSKUID
            __typename
        }
        socialProof {
            bgColor
            contents {
            name
            content
            iconURL
            __typename
            }
            __typename
        }
        __typename
        }
        
        fragment PdpDataProductMedia on pdpDataProductMedia {
        media {
            type
            suffix
            prefix
            URLThumbnail
            URLOriginal
            videoURLAndroid
            URLMaxRes
            description
            index
            variantOptionID
            __typename
        }
        recommendation {
            lightIcon
            darkIcon
            iconText
            bottomsheetTitle
            recommendation
            __typename
        }
        videos {
            source
            url
            __typename
        }
        containerType
        liveIndicator {
            isLive
            channelID
            mediaURL
            applink
            __typename
        }
        showJumpToVideo
        __typename
        }
        
        fragment PdpDataProductContent on pdpDataProductContent {
        name
        parentName
        price {
            value
            currency
            priceFmt
            slashPriceFmt
            discPercentage
            __typename
        }
        campaign {
            campaignID
            campaignType
            campaignTypeName
            percentageAmount
            originalPrice
            discountedPrice
            originalStock
            stock
            stockSoldPercentage
            threshold
            startDate
            endDate
            endDateUnix
            appLinks
            isAppsOnly
            isActive
            hideGimmick
            campaignIdentifier
            applink
            background
            paymentInfoWording
            __typename
        }
        thematicCampaign {
            ...PDPThematicCampaign
            __typename
        }
        stock {
            useStock
            value
            stockWording
            __typename
        }
        variant {
            isVariant
            parentID
            __typename
        }
        wholesale {
            minQty
            price {
            value
            currency
            __typename
            }
            __typename
        }
        isCashback {
            percentage
            __typename
        }
        isOS
        isPowerMerchant
        isWishlist
        isCOD
        isShowPrice
        preorder {
            duration
            timeUnit
            isActive
            preorderInDays
            __typename
        }
        labelIcons {
            ...PDPContentLabelIcon
            __typename
        }
        __typename
        }
        
        fragment PdpDataCustomInfo on pdpDataCustomInfo {
        icon
        title
        isApplink
        lightIcon
        applink
        separator
        description
        label {
            value
            color
            __typename
        }
        __typename
        }
        
        fragment PdpDataProductDetail on pdpDataProductDetail {
        content {
            key
            type
            action
            extParam
            title
            subtitle
            applink
            showAtFront
            isAnnotation
            showAtBottomsheet
            icon
            webLink {
            action
            query
            __typename
            }
            __typename
        }
        title
        bottomsheet {
            actionTitle
            param
            bottomSheetTitle
            __typename
        }
        __typename
        }
        
        fragment PdpDataUpcomingCampaign on pdpDataUpcomingCampaign {
        campaignID
        campaignType
        campaignTypeName
        startDate
        endDate
        notifyMe
        ribbonCopy
        upcomingType
        productID
        descriptionHeader
        timerWording
        bgColor
        __typename
        }
        
        fragment PdpDataCategoryCarousel on pdpDataCategoryCarousel {
        linkText
        titleCarousel
        applink
        list {
            categoryID
            icon
            title
            isApplink
            applink
            __typename
        }
        __typename
        }
        
        fragment PdpDataProductInfo on pdpDataProductInfo {
        row
        content {
            title
            subtitle
            applink
            __typename
        }
        __typename
        }
        
        fragment PdpDataInfo on pdpDataInfo {
        icon
        lightIcon
        title
        isApplink
        applink
        content {
            icon
            text
            __typename
        }
        __typename
        }
        
        fragment PdpDataSocialProof on pdpDataSocialProof {
        row
        content {
            icon
            title
            subtitle
            applink
            type
            rating
            __typename
        }
        __typename
        }
        
        fragment PdpDataOneLiner on pdpDataOneLiner {
        productID
        oneLinerContent
        color
        linkText
        applink
        separator
        icon
        isVisible
        eduLink {
            webLink {
            action
            query
            __typename
            }
            __typename
        }
        __typename
        }
        
        fragment PdpDataOneLinerVariant on pdpDataComponentDynamicOneLinerVariant {
        name
        text
        applink
        separator
        icon
        status
        chevronPos
        padding {
            t
            b
            __typename
        }
        imageSize {
            w
            h
            __typename
        }
        bgColor
        chevronColor
        __typename
        }
        
        fragment PdpDataDynamicOneLiner on pdpDataDynamicOneLiner {
        name
        text
        applink
        separator
        icon
        status
        chevronPos
        padding {
            t
            b
            __typename
        }
        imageSize {
            w
            h
            __typename
        }
        bgColor
        chevronColor
        __typename
        }
        
        fragment pdpDataCustomInfoTitle on pdpDataCustomInfoTitle {
        title
        status
        componentName
        __typename
        }
        
        fragment PdpDataOnGoingCampaign on pdpDataOnGoingCampaign {
        isReleased
        campaign {
            ...PDPOngoingCampaign
            __typename
        }
        thematicCampaign {
            ...PDPThematicCampaign
            __typename
        }
        variantCampaign {
            campaigns {
            ...PDPOngoingCampaign
            __typename
            }
            thematicCampaigns {
            ...PDPThematicCampaign
            __typename
            }
            __typename
        }
        __typename
        }
        
        fragment PDPOngoingCampaign on pdpContentSnapshotCampaign {
        campaignID
        campaignType
        campaignTypeName
        campaignLogo
        percentageAmount
        originalPrice
        discountedPrice
        originalStock
        stock
        stockSoldPercentage
        threshold
        startDate
        endDate
        endDateUnix
        appLinks
        isAppsOnly
        isActive
        hideGimmick
        campaignIdentifier
        background
        paymentInfoWording
        productID
        campaignLogo
        applink
        stockWording
        stockIcon
        showStockBar
        __typename
        }
        
        fragment PdpDataProductDetailMediaComponent on pdpDataProductDetailMediaComponent {
        title
        description
        contentMedia {
            url
            ratio
            type
            __typename
        }
        show
        ctaText
        __typename
        }
        
        fragment PdpDataComponentSocialProofV2 on pdpDataComponentSocialProofV2 {
        socialProofContent {
            socialProofType
            socialProofID
            title
            subtitle
            icon
            applink {
            webLink {
                action
                query
                __typename
            }
            __typename
            }
            URL
            hasSeparator
            bgColor
            showChevron
            chevronColor
            __typename
        }
        __typename
        }
        
        fragment PdpDataComponentSDUIDivKit on pdpDataComponentSDUIDivKit {
        template
        state
        __typename
        }
        
        fragment PdpDataProductListComponent on pdpDataProductListComponent {
        queryParam
        thematicID
        __typename
        }
        
        fragment PDPThematicCampaign on pdpContentSnapshotThematicCampaign {
        campaignName
        campaignLogo
        background
        icon
        additionalInfo
        productID
        applink
        superGraphicURL
        __typename
        }
        
        fragment PdpDataComponentPromoPrice on pdpDataComponentPromoPrice {
        price {
            value
            currency
            lastUpdateUnix
            priceFmt
            slashPriceFmt
            discPercentage
            isPriceMasked
            valueFmt
            currencyFmt
            __typename
        }
        promoType
        promo {
            ...PDPDataPromo
            __typename
        }
        background
        componentPriceType
        __typename
        }
        
        fragment PDPDataPromo on pdpDataPromo {
        value
        iconURL
        productID
        promoPriceFmt
        subtitle
        applink
        color
        background
        promoType
        superGraphicURL
        separatorColor
        priceAdditionalFmt
        promoCodes {
            ...PDPDataPromoCode
            __typename
        }
        bottomsheetParam
        __typename
        }
        
        fragment PDPDataPromoCode on pdpDataPromoCode {
        promoID
        promoCode
        promoCodeType
        __typename
        }
        
        fragment PDPContentLabelIcon on pdpContentLabelIcon {
        label
        iconURL
        type
        __typename
        }
        
        fragment PdpDataComponentShipmentV4 on pdpDataComponentShipmentV4 {
        data {
            productID
            warehouse_info {
            warehouse_id
            is_fulfillment
            district_id
            postal_code
            geolocation
            city_name
            ttsWarehouseID
            __typename
            }
            useBOVoucher
            isCOD
            metadata
            __typename
        }
        __typename
        }
        
        fragment PdpDataComponentShipmentV5 on pdpDataComponentShipmentV5 {
        data {
            productID
            warehouse_info {
            warehouse_id
            is_fulfillment
            district_id
            postal_code
            geolocation
            city_name
            ttsWarehouseID
            __typename
            }
            useBOVoucher
            isCOD
            metadata
            __typename
        }
        __typename
        }
        
        fragment PdpDataComponentAffordabilityGroupLabel on pdpDataAffordabilityGroupLabel {
        affordabilityData {
            productID
            productVouchers {
            identifier
            type
            text
            backgroundColor
            __typename
            }
            showChevron
            chevronColor
            appliedVoucherTypeIDs
            __typename
        }
        __typename
        }
        """
        }
        try:
            res = requests.post(urlQuery, headers=headerProductPage, json=payload)
        except Exception:
            return None
        time.sleep(0.5)
        return res.json()
    
    def save_to_csv(self,all_products, filename="tokopedia_products.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file,quoting=csv.QUOTE_ALL)
            writer.writerow(["Product Name", "Product URL", "Price", "Shop Name", "City","Rating",'Description'])
            for product in all_products:            
                writer.writerow([
                    product["name"],
                    product["url"],
                    self.parse_price(product["price"]["text"]) if product.get("price") else "",
                    product["shop"]["name"] if product.get("shop") else "",
                    product["shop"]["city"] if product.get("shop") else "",
                    float(product["rating"]) if product.get("rating") else "",
                    product["product_detail"] if product.get("product_detail") else "",
                ])
        print(f"Saved to {filename}")

    def append_to_csv(self,all_products, filename="tokopedia_products.csv"):
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file,quoting=csv.QUOTE_ALL)
            writer.writerow(["Product Name", "Product URL", "Price", "Shop Name", "City","Rating",'Description'])
            for product in all_products:            
                writer.writerow([
                    product["name"],
                    product["url"],
                    self.parse_price(product["price"]["text"]) if product.get("price") else "",
                    product["shop"]["name"] if product.get("shop") else "",
                    product["shop"]["city"] if product.get("shop") else "",
                    float(product["rating"]) if product.get("rating") else "",
                    product["product_detail"] if product.get("product_detail") else "",
                ])
        print(f"[{time.strftime('%Y-%m_%d-%H-%M-%S', time.gmtime())}] Append to {filename}")
    
    def fetch_all_products(self,max_pages=0):
        url = "https://gql.tokopedia.com/graphql/SearchProductV5Query"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(self.userAgentList),
            "Accept": "*/*",
            'Origin': 'https://www.tokopedia.com',
            'Referer': 'https://www.tokopedia.com/',
        }
        
        all_products = []
        next_offset = 0
        search_id = ""
        minus_ids = ""
        ads_minus_ids = ""

        state = True
        page = 0

        while True:
            print(f"[{time.strftime('%Y-%m_%d-%H-%M-%S', time.gmtime())}] 🌐 Fetching {url} for Page {page+1}")

            payload = {
                "operationName": "SearchProductV5Query",
                "variables": {
                    "searchProductV5Param": f"device=mobile&enable_lite_deduplication=true&enter_method=normal_search&q={self.keyword}&rows=8&page=1&source=search&use_page=true&next_offset={next_offset}&search_id={search_id}&minus_ids={minus_ids}"
                },
                "query": """query SearchProductV5Query($searchProductV5Param: String!) {
                searchProductV5(params: $searchProductV5Param) {
                    header {
                    additionalParams
                    }
                    data {
                    products {
                        id
                        name
                        url
                        price {
                        text
                        }
                        shop {
                        name
                        city
                        }
                        rating
                    }
                    }
                }
                }"""
            }

            try:
                res = requests.post(url, headers=headers, json=payload)

                if res.status_code == 200:
                    data = res.json()
                    products = data['data']['searchProductV5']['data']['products']

                    for i in range(len(products)):
                        try:
                            product_page = self.get_product_page(products[i]['url'])
                            if product_page != None:
                                products[i]['product_detail'] = product_page['data']['pdpGetLayout']['components'][21]['data'][0]['content'][-1]['subtitle'] if product_page['data']['pdpGetLayout']['components'][21]['data'][0]['content'][-1]['subtitle'] else ""
                            else :
                                products[i]['product_detail'] = ""
                        except Exception as e:
                            products[i]['product_detail'] = ""
                            print(e)
                            continue;
                        
                    all_products.extend(products)

                    additional_params = data['data']['searchProductV5']['header']['additionalParams']
                    # print("Additional Params = ",additional_params)
                    if "next_offset=" in additional_params and "search_id=" in additional_params:
                        from urllib.parse import parse_qs
                        query_parts = parse_qs(additional_params.replace("?", "").replace("\\u0026", "&"))
                        next_offset = query_parts.get("next_offset", [None])[0]
                        search_id = query_parts.get("search_id", [None])[0]
                        minus_ids = query_parts.get("minus_ids", [None])[0]
                        ads_minus_ids = query_parts.get("ads_minus_ids", [None])[0]
                    else:
                        break 
                else :
                    raise Exception("Status Code not 200")
            except Exception as e:
                print(e)
                continue;
            except KeyboardInterrupt:
                print("Keyboard Interupt")
                if self.type == "a":
                    self.append_to_csv(products,self.csvFile)
                return all_products
            
            if self.type == "a":
                self.append_to_csv(products,self.csvFile)
            page += 1

            if(max_pages != 0 and page >= max_pages):
                break
            print()
            time.sleep(2)

        return all_products

