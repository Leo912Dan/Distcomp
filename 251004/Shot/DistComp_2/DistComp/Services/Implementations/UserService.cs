﻿using AutoMapper;
using DistComp.DTO.RequestDTO;
using DistComp.DTO.ResponseDTO;
using DistComp.Exceptions;
using DistComp.Infrastructure.Validators;
using DistComp.Models;
using DistComp.Repositories.Interfaces;
using DistComp.Services.Interfaces;
using FluentValidation;
using ValidationException = System.ComponentModel.DataAnnotations.ValidationException;

namespace DistComp.Services.Implementations;

public class UserService : IUserService
{
    private readonly IUserRepository _userRepository;
    private readonly IMapper _mapper;
    private readonly UserRequestDTOValidator _validator;
    
    public UserService(IUserRepository userRepository, 
        IMapper mapper, UserRequestDTOValidator validator)
    {
        _userRepository = userRepository;
        _mapper = mapper;
        _validator = validator;
    }
    
    public async Task<IEnumerable<UserResponseDTO>> GetUsersAsync()
    {
        var users = await _userRepository.GetAllAsync();
        return _mapper.Map<IEnumerable<UserResponseDTO>>(users);
    }

    public async Task<UserResponseDTO> GetUserByIdAsync(long id)
    {
        var user = await _userRepository.GetByIdAsync(id)
                      ?? throw new NotFoundException(ErrorCodes.UserNotFound, ErrorMessages.UserNotFoundMessage(id));
        return _mapper.Map<UserResponseDTO>(user);
    }

    public async Task<UserResponseDTO> CreateUserAsync(UserRequestDTO user)
    {
        await _validator.ValidateAndThrowAsync(user);
        var userToCreate = _mapper.Map<User>(user);
        var createdUser = await _userRepository.CreateAsync(userToCreate);
        return _mapper.Map<UserResponseDTO>(createdUser);
    }

    public async Task<UserResponseDTO> UpdateUserAsync(UserRequestDTO user)
    {
        await _validator.ValidateAndThrowAsync(user);
        var userToUpdate = _mapper.Map<User>(user);
        var updatedUser = await _userRepository.UpdateAsync(userToUpdate)
                             ?? throw new NotFoundException(ErrorCodes.UserNotFound, ErrorMessages.UserNotFoundMessage(user.Id));
        return _mapper.Map<UserResponseDTO>(updatedUser);
    }

    public async Task DeleteUserAsync(long id)
    {
        if (!await _userRepository.DeleteAsync(id))
        {
            throw new NotFoundException(ErrorCodes.UserNotFound, ErrorMessages.UserNotFoundMessage(id));
        }
    }
}