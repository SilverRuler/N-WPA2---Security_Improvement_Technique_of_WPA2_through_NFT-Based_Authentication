// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC721/ERC721.sol)

pragma solidity ^0.8.7;

import "./extensions/ERC721URIStorage.sol";
import "./utils/Context.sol";

/**
 * @dev Implementation of https://eips.ethereum.org/EIPS/eip-721[ERC721] Non-Fungible Token Standard, including
 * the Metadata extension, but not including the Enumerable extension, which is available separately as
 * {ERC721Enumerable}.  
 */
contract NWPA2 is ERC721URIStorage {
    uint256 private _tokenId;
    

    string private SSID = '123123';
    string private PW = '321321';
    mapping(address => uint) private map_addr;
    bool use_whitelist = true;

    constructor() public ERC721("NFT AUTH", "NAUTH") {
    }

    function _increment() private {
        _tokenId += 1;
    }

    function current() public view returns (uint256) {
        return _tokenId;
    }

    function genNew(string memory _tokenURI, address to) public returns (uint256) {
        _increment();
        uint256 newTokenId = current();

        _mint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, _tokenURI);
        _transfer(msg.sender, to, newTokenId);

        return newTokenId;
    }

    /**SP section */
    function chagneSP(string memory newSSID, string memory newPW) public {
        SSID = newSSID;
        PW = newPW;
    }
    
    function getSSID() public view returns (string memory) {
        return SSID;
    }

    function getPW() public view returns (string memory) {
        return PW;
    }

    /**whitelist section */
    function is_whitelistNFT(address addr) public view returns(uint) {
        return map_addr[addr];
    }

    function add_whitelistNFT(address a) public {
        require(map_addr[a] == 0);

        map_addr[a] = 1;
    }

    function del_whitelistNFT(address a) public {
        require(map_addr[a] != 0);

        // map_data[a] = 0;
        delete map_addr[a];
    }

}
