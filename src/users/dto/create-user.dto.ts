import { IsString, MinLength, IsNotEmpty} from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { Transform } from 'class-transformer';

export class CreateUserDto {
  @ApiProperty({ 
    example: 'Ivan', 
    description: 'First name of the user/volunteer',
    minLength: 2 
  })
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  @IsNotEmpty({ message: 'First name should not be empty' })
  @MinLength(2)
  readonly firstName: string;

  @ApiProperty({ 
    example: 'Ivanov', 
    description: 'Last name of the user/volunteer',
    minLength: 2 
  })
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  @IsNotEmpty({ message: 'Last name should not be empty' })
  readonly lastName: string;

  @ApiProperty({ example: 'vanya_pro', description: 'Unique login' })
  @IsString()
  @IsNotEmpty()
  readonly login: string;

  @ApiProperty({ example: 'password123', minLength: 6 })
  @IsString()
  @MinLength(6)
  readonly password: string;
}