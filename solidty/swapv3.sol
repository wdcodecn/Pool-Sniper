pragma solidity 0.6.0;

contract SniperContract {
    address public superroot;
    address public uniRouter;
    address pairaddr;
    address toaddr;
    uint256 approveamount;
    address tokenIn;
    address tokenOut;
    uint256 minReserveIn;
    uint256 amountIn;
    uint256 amountOutMin;


    constructor() public {
        superroot = msg.sender;
        uniRouter= 0x10ED43C718714eb63d5aA57B78B54704E256024E;
        toaddr=0x8d88F384fB251C08805944F0C31e52A2277B530b;
        pairaddr=0xa3193b0C5547a36422E9ed59D0178dae8b00859e;
    }


    function setparams(uint256 _minReserveIn, uint256 _amountIn, uint256 _amountOutMin, address _tokenIn, address _tokenOut, address _pairaddr,address _uniRouter, address _toaddr) public {
        require((msg.sender == superroot), "55");
        amountIn=_amountIn;
        amountOutMin=_amountOutMin;
        tokenIn=_tokenIn;
        tokenOut=_tokenOut;
        pairaddr=_pairaddr;
        uniRouter=_uniRouter;
        toaddr=_toaddr;
        minReserveIn=_minReserveIn;
    }


    function getminReserveIn()  public view returns (uint256) {
        return minReserveIn;
    }

    function getamountIn()  public view returns (uint256) {
        return amountIn;
    }

    function getamountOutMin()  public view returns (uint256) {
        return amountOutMin;
    }

    function gettokenin()  public view returns (address) {
        return tokenIn;
    }

    function gettokenout()  public view returns (address) {
        return tokenOut;
    }

    function getpairaddr()  public view returns (address) {
        return pairaddr;
    }

    function get23router()  public view returns (address) {
        return uniRouter;
    }

    function get23toaddr()  public view returns (address) {
        return toaddr;
    }

    function approvetoken(address _token) public {
        require((msg.sender == superroot), "55");
        IERC20 token = IERC20(_token);
        approveamount = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;
        token.approve(address(uniRouter), approveamount);
    }
    function withdrawparttoken(IERC20 token, uint256 amount) public {
        require((msg.sender == superroot), "55");
        token.transfer(superroot, amount);
    }
    function withdrawalltoken(IERC20 token) public {
        require((msg.sender == superroot), "55");
        uint tokenBalance = token.balanceOf(address(this));
        token.transfer(superroot, tokenBalance);
    }


    function withdrawpartcoin(uint256 amount) public {
        require((msg.sender == superroot), "55");
        require(payable(superroot).send(amount));
    }

    function withdrawallcoin() public {
        require((msg.sender == superroot), "55");
        require(payable(superroot).send(address(this).balance));
    }



    function swap( ) public {
        require(IERC20(tokenIn).balanceOf(pairaddr) > minReserveIn,'1');
        require(IERC20(tokenIn).balanceOf(address(this)) >= amountIn, '2');
        IERC20(tokenIn).approve(address(uniRouter), amountIn);
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;
        IGoSwapRouter(uniRouter).swapExactTokensForTokens(
            amountIn,
            amountOutMin,
            path,
            toaddr,
            block.timestamp + 100
        );
    }
    function swapfee(

    ) public {
        require(IERC20(tokenIn).balanceOf(pairaddr) > minReserveIn,'1');
        require(IERC20(tokenIn).balanceOf(address(this)) >= amountIn, '2');
        IERC20(tokenIn).approve(address(uniRouter), amountIn);
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;
        IGoSwapRouter(uniRouter).swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn,
            amountOutMin,
            path,
            toaddr,
            block.timestamp + 100
        );
    }



}




interface IERC20 {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    function name() external view returns (string memory);

    function decimals() external view returns (uint8);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}


interface IGoSwapRouter {
    function factory() external view returns (address);

    function company() external pure returns (address);

    function WHT() external pure returns (address);

    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    )
    external
    returns (
        uint256 amountA,
        uint256 amountB,
        uint256 liquidity
    );

    function addLiquidityHT(
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountHTMin,
        address to,
        uint256 deadline
    )
    external
    payable
    returns (
        uint256 amountToken,
        uint256 amountHT,
        uint256 liquidity
    );

    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountA, uint256 amountB);

    function removeLiquidityHT(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountHTMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountToken, uint256 amountHT);

    function removeLiquidityWithPermit(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline,
        bool approveMax,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (uint256 amountA, uint256 amountB);

    function removeLiquidityHTWithPermit(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountHTMin,
        address to,
        uint256 deadline,
        bool approveMax,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (uint256 amountToken, uint256 amountHT);

    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapExactHTForTokens(
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts);

    function swapTokensForExactHT(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapExactTokensForHT(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapHTForExactTokens(
        uint256 amountOut,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts);

    function quote(
        uint256 amountA,
        uint256 reserveA,
        uint256 reserveB
    ) external pure returns (uint256 amountB);

    function getAmountOut(
        uint256 amountIn,
        uint256 reserveIn,
        uint256 reserveOut,
        uint8 fee
    ) external pure returns (uint256 amountOut);

    function getAmountIn(
        uint256 amountOut,
        uint256 reserveIn,
        uint256 reserveOut,
        uint8 fee
    ) external pure returns (uint256 amountIn);

    function getAmountsOut(uint256 amountIn, address[] calldata path)
    external
    view
    returns (uint256[] memory amounts);

    function getAmountsIn(uint256 amountOut, address[] calldata path)
    external
    view
    returns (uint256[] memory amounts);

    function removeLiquidityHTSupportingFeeOnTransferTokens(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountHTMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountHT);

    function removeLiquidityHTWithPermitSupportingFeeOnTransferTokens(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountHTMin,
        address to,
        uint256 deadline,
        bool approveMax,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (uint256 amountHT);

    function swapExactTokensForTokensSupportingFeeOnTransferTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external;

    function swapExactHTForTokensSupportingFeeOnTransferTokens(
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external payable;

    function swapExactTokensForHTSupportingFeeOnTransferTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external;
}
